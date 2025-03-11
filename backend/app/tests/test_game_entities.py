import pytest
from fastapi.testclient import TestClient
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

# Player endpoint tests
def test_create_player(sample_player):
    response = client.post("/api/v1/players/", json=sample_player)
    assert response.status_code == 501  # Not implemented yet
    # When implemented:
    # assert response.status_code == 200
    # assert response.json()["name"] == sample_player["name"]

def test_get_player():
    response = client.get("/api/v1/players/TestPlayer")
    assert response.status_code == 501  # Not implemented yet
    # When implemented:
    # assert response.status_code == 200
    # assert response.json()["name"] == "TestPlayer"

# Planet endpoint tests
def test_get_planet():
    response = client.get("/api/v1/planets/test-planet-id")
    assert response.status_code == 501  # Not implemented yet
    # When implemented:
    # assert response.status_code == 200
    # assert response.json()["id"] == "test-planet-id"

def test_colonize_planet():
    response = client.patch(
        "/api/v1/planets/test-planet-id/colonize",
        params={"player_name": "TestPlayer"}
    )
    assert response.status_code == 501  # Not implemented yet
    # When implemented:
    # assert response.status_code == 200
    # assert response.json()["colonized"] == True
    # assert response.json()["owner"] == "TestPlayer"

# Game State endpoint tests
def test_create_game(sample_game_state):
    response = client.post("/api/v1/games/", json=sample_game_state)
    assert response.status_code == 501  # Not implemented yet
    # When implemented:
    # assert response.status_code == 200
    # assert response.json()["id"] == sample_game_state["id"]

def test_get_game_state():
    response = client.get("/api/v1/games/test-game-id")
    assert response.status_code == 501  # Not implemented yet
    # When implemented:
    # assert response.status_code == 200
    # assert response.json()["id"] == "test-game-id"

def test_advance_turn():
    response = client.patch("/api/v1/games/test-game-id/turn")
    assert response.status_code == 501  # Not implemented yet
    # When implemented:
    # assert response.status_code == 200
    # assert response.json()["turn"] == 2  # Turn should increment 