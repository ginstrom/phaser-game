import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

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
from app.database.config import Base, get_db
from app.database.models import (
    Game as GameDB,
    Planet as PlanetDB,
    PlayerResources as PlayerResourcesDB,
    Galaxy as GalaxyDB
)

# Create in-memory test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create test database tables
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture
def sample_player():
    return {
        "name": "TestPlayer",
        "empire": "Test Empire",
        "resources": {
            "organic": 0,
            "mineral": 500,
            "energy": 200,
            "exotics": 0,
            "credits": 1000,
            "research": 0
        }
    }

@pytest.fixture
def sample_planet():
    return {
        "id": "test-planet-id",
        "name": "Test Planet",
        "type": PlanetType.TERRESTRIAL.value,
        "size": 5,
        "resources": {
            "organic": 50,
            "mineral": 50,
            "energy": 50,
            "exotics": 50
        },
        "colonized": False,
        "owner": None
    }

@pytest.fixture
def sample_game_state(sample_player):
    return {
        "id": "test-game-id",
        "player": sample_player,
        "galaxy": {
            "size": GalaxySize.SMALL.value,
            "systems": [],
            "explored_count": 0
        },
        "turn": 1,
        "difficulty": Difficulty.NORMAL.value
    }

@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def test_game(db_session, sample_player):
    # Create test game in database
    game = GameDB(
        id="test-game-id",
        player_name=sample_player["name"],
        empire_name=sample_player["empire"],
        difficulty=Difficulty.NORMAL.value,
        galaxy_size=GalaxySize.SMALL.value
    )
    
    resources = PlayerResourcesDB(
        game=game,
        **sample_player["resources"]
    )
    
    galaxy = GalaxyDB(
        game=game,
        size=GalaxySize.SMALL.value
    )
    
    db_session.add(game)
    db_session.add(resources)
    db_session.add(galaxy)
    db_session.commit()
    
    return game

@pytest.fixture
def test_planet(db_session, test_game):
    # Create test planet in database
    planet = PlanetDB(
        id="test-planet-id",
        system_id="test-system-id",
        name="Test Planet",
        type=PlanetType.TERRESTRIAL.value,
        size=5
    )
    db_session.add(planet)
    db_session.commit()
    return planet

# Player endpoint tests
def test_create_player(sample_player):
    response = client.post("/api/v1/players/", json=sample_player)
    assert response.status_code == 200
    assert response.json()["name"] == sample_player["name"]
    assert response.json()["empire"] == sample_player["empire"]
    assert response.json()["resources"] == sample_player["resources"]

def test_get_player(test_game):
    response = client.get(f"/api/v1/players/{test_game.player_name}")
    assert response.status_code == 200
    assert response.json()["name"] == test_game.player_name
    assert response.json()["empire"] == test_game.empire_name

def test_get_nonexistent_player():
    response = client.get("/api/v1/players/NonexistentPlayer")
    assert response.status_code == 404

# Planet endpoint tests
def test_get_planet(test_planet):
    response = client.get(f"/api/v1/planets/{test_planet.id}")
    assert response.status_code == 200
    assert response.json()["id"] == test_planet.id
    assert response.json()["name"] == test_planet.name

def test_get_nonexistent_planet():
    response = client.get("/api/v1/planets/nonexistent-id")
    assert response.status_code == 404

def test_colonize_planet(test_planet, test_game):
    response = client.patch(
        f"/api/v1/planets/{test_planet.id}/colonize",
        params={"player_name": test_game.player_name}
    )
    assert response.status_code == 200
    assert response.json()["colonized"] == True
    assert response.json()["owner"] == test_game.id

def test_colonize_nonexistent_planet(test_game):
    response = client.patch(
        "/api/v1/planets/nonexistent-id/colonize",
        params={"player_name": test_game.player_name}
    )
    assert response.status_code == 404

def test_colonize_already_colonized_planet(test_planet, test_game, db_session):
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
def test_create_game(sample_game_state):
    response = client.post("/api/v1/games/", json=sample_game_state)
    assert response.status_code == 200
    assert response.json()["player"]["name"] == sample_game_state["player"]["name"]
    assert response.json()["difficulty"] == sample_game_state["difficulty"]
    assert response.json()["turn"] == sample_game_state["turn"]

def test_get_game_state(test_game):
    response = client.get(f"/api/v1/games/{test_game.id}")
    assert response.status_code == 200
    assert response.json()["id"] == test_game.id
    assert response.json()["player"]["name"] == test_game.player_name
    assert response.json()["turn"] == test_game.turn

def test_get_nonexistent_game():
    response = client.get("/api/v1/games/nonexistent-id")
    assert response.status_code == 404

def test_advance_turn(test_game):
    initial_turn = test_game.turn
    response = client.patch(f"/api/v1/games/{test_game.id}/turn")
    assert response.status_code == 200
    assert response.json()["turn"] == initial_turn + 1

def test_advance_turn_nonexistent_game():
    response = client.patch("/api/v1/games/nonexistent-id/turn")
    assert response.status_code == 404 