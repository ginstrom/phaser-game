import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
import uuid

from app.main import app
from app.models.game import (
    Player,
    PlayerResources,
    Planet,
    PlanetResources,
    StarSystem,
    Galaxy,
    GameState
)
from app.config import PlanetType, GalaxySize, Difficulty
from app.database.models import (
    Game as GameDB,
    Planet as PlanetDB,
    PlayerResources as PlayerResourcesDB,
    PlanetResources as PlanetResourcesDB,
    Galaxy as GalaxyDB,
    Empire,
    StarSystem as StarSystemDB
)
from app.models.empire import EmpireDB

@pytest.fixture
def test_game(db_session: Session, sample_player):
    """Create a test game in the database."""
    game = GameDB(
        id=str(uuid.uuid4()),
        player_name=sample_player["name"],
        difficulty=Difficulty.NORMAL.value,
        galaxy_size=GalaxySize.SMALL.value
    )
    
    resources = PlayerResourcesDB(
        id=str(uuid.uuid4()),
        game=game,
        **sample_player["resources"]
    )
    
    galaxy = GalaxyDB(
        id=str(uuid.uuid4()),
        game=game,
        size=GalaxySize.SMALL.value
    )
    
    # Create player empire
    empire = EmpireDB(
        game=game,
        name=f"{sample_player['name']}'s Empire",
        is_player=True,
        color="#00FF00"
    )
    
    db_session.add(game)
    db_session.add(resources)
    db_session.add(galaxy)
    db_session.add(empire)
    db_session.flush()
    
    # Update game with player empire
    game.player_empire_id = empire.id
    db_session.commit()
    
    return game

@pytest.fixture
def test_planet(db_session: Session, test_game: GameDB):
    """Create a test planet in the database."""
    # Create test star system
    system = StarSystemDB(
        id=str(uuid.uuid4()),
        galaxy=test_game.galaxy,
        name="Test System",
        position_x=0.5,
        position_y=0.5
    )
    db_session.add(system)
    db_session.flush()

    # Create test planet in database
    planet = PlanetDB(
        id=str(uuid.uuid4()),
        system=system,
        name="Test Planet",
        type=PlanetType.TERRESTRIAL.value,
        size=5,
        colonized=False,
        empire_id=None
    )
    db_session.add(planet)
    db_session.flush()
    
    # Create planet resources
    resources = PlanetResourcesDB(
        id=str(uuid.uuid4()),
        planet=planet,
        organic=50,
        mineral=50,
        energy=50,
        exotics=50
    )
    db_session.add(resources)
    db_session.commit()
    
    return planet

# Player endpoint tests
def test_create_player(client: TestClient, sample_player):
    """Test creating a new player."""
    response = client.post("/api/v1/players/", json=sample_player)
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == sample_player["name"]
    assert "empire" in data
    assert "name" in data["empire"]

def test_get_player(client: TestClient, test_game: GameDB):
    """Test getting a player by name."""
    response = client.get(f"/api/v1/players/{test_game.player_name}")
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == test_game.player_name
    assert "empire" in data
    assert "name" in data["empire"]

def test_get_nonexistent_player(client: TestClient):
    """Test getting a nonexistent player."""
    response = client.get("/api/v1/players/NonexistentPlayer")
    assert response.status_code == 404

# Planet endpoint tests
def test_get_planet(client: TestClient, test_planet: PlanetDB):
    """Test getting a planet by ID."""
    response = client.get(f"/api/v1/planets/{test_planet.id}")
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == test_planet.id
    assert "name" in data

def test_get_nonexistent_planet(client: TestClient):
    """Test getting a nonexistent planet."""
    response = client.get("/api/v1/planets/nonexistent-id")
    assert response.status_code == 404

def test_colonize_planet(client: TestClient, test_planet: PlanetDB, test_game: GameDB):
    """Test colonizing a planet."""
    response = client.patch(
        f"/api/v1/planets/{test_planet.id}/colonize",
        params={"player_name": test_game.player_name}
    )
    data = response.json()
    assert response.status_code == 200
    assert "colonized" in data
    assert "owner" in data

def test_colonize_already_colonized_planet(client: TestClient, test_planet: PlanetDB, test_game: GameDB, db_session: Session):
    """Test colonizing an already colonized planet."""
    # First colonization
    test_planet.colonized = True
    test_planet.empire_id = test_game.id
    db_session.commit()
    
    # Try to colonize again
    response = client.patch(
        f"/api/v1/planets/{test_planet.id}/colonize",
        params={"player_name": test_game.player_name}
    )
    assert response.status_code == 400

# Game State endpoint tests
def test_create_game(client: TestClient, sample_game_state):
    """Test creating a new game."""
    response = client.post("/api/v1/games/", json=sample_game_state)
    data = response.json()
    assert response.status_code == 200
    assert "player" in data
    assert data["player"]["name"] == sample_game_state["player"]["name"]
    assert "empire" in data["player"]
    assert "name" in data["player"]["empire"]
    assert "difficulty" in data
    assert "galaxy" in data
    assert "size" in data["galaxy"]

def test_get_game_state(client: TestClient, test_game: GameDB):
    """Test getting game state."""
    response = client.get(f"/api/v1/games/{test_game.id}/state")
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == test_game.id
    assert "player" in data
    assert data["player"]

def test_get_game_state_nonexistent_game(client: TestClient):
    """Test getting state of a nonexistent game."""
    response = client.get("/api/v1/games/nonexistent-id/state")
    assert response.status_code == 404

def test_advance_turn(client: TestClient, test_game: GameDB):
    """Test advancing game turn."""
    initial_turn = test_game.turn
    response = client.patch(f"/api/v1/games/{test_game.id}/advance-turn")
    data = response.json()
    assert response.status_code == 200
    assert "turn" in data
    assert data["turn"] > initial_turn

def test_advance_turn_nonexistent_game(client: TestClient):
    """Test advancing turn of a nonexistent game."""
    response = client.patch("/api/v1/games/nonexistent-id/advance-turn")
    assert response.status_code == 404 