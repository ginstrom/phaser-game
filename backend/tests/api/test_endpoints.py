import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Set test environment
os.environ["ENVIRONMENT"] = "test"

from app.main import app
from app.database.models import Game
from app.models.empire import EmpireDB

@pytest.fixture
def test_game(db_session):
    """Create a test game."""
    game = Game(
        player_name="TestPlayer",
        difficulty="normal",
        galaxy_size="medium"
    )
    db_session.add(game)
    db_session.commit()
    db_session.refresh(game)
    return game

def test_get_game_endpoint(client: TestClient, test_game: Game):
    """Test getting a game by ID."""
    response = client.get(f"/api/v1/games/{test_game.id}/state")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_game.id
    assert data["player_name"] == test_game.player_name

def test_list_games_endpoint(client: TestClient, test_game: Game):
    """Test listing all games."""
    response = client.get("/api/v1/games/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert any(game["id"] == test_game.id for game in data)

def test_delete_game_endpoint(client: TestClient, test_game: Game):
    """Test deleting a game."""
    response = client.delete(f"/api/v1/games/{test_game.id}/")
    assert response.status_code == 200
    
    # Verify game was deleted
    response = client.get(f"/api/v1/games/{test_game.id}/state")
    assert response.status_code == 404

# Tests
def test_root_endpoint(client: TestClient):
    """Test the root endpoint returns correct welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to the 4X Space Empire API"
    assert data["version"] == "0.1.0"
    assert data["documentation"] == "/docs"

class TestNewGameEndpoint:
    def test_create_new_game_success(self, client: TestClient):
        """Test creating a new game with valid parameters."""
        response = client.post("/api/v1/games/new", json={
            "player_name": "TestPlayer",
            "galaxy_size": "medium",
            "difficulty": "normal"
        })
        assert response.status_code == 200
        data = response.json()
        assert "game_id" in data
        assert "message" in data
        assert "initial_state" in data
        # Check for essential keywords in a case-insensitive way
        message = data["message"].lower()
        assert "new" in message
        assert "game" in message
        assert "created" in message
        assert "testplayer" in message  # Player name should be included

    def test_create_new_game_invalid_data(self, client: TestClient):
        """Test creating a new game with invalid parameters."""
        response = client.post("/api/v1/games/new", json={
            "player_name": "",  # Empty name should be invalid
            "galaxy_size": "invalid",  # Invalid size
            "difficulty": "invalid"  # Invalid difficulty
        })
        assert response.status_code == 422

class TestLoadGameEndpoint:
    def test_load_game_success(self, client: TestClient, test_game_id: str):
        """Test loading an existing game."""
        response = client.get(f"/api/v1/games/{test_game_id}/state")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_game_id
        assert "game_state" in data
        assert "empires" in data

    def test_load_nonexistent_game(self, client: TestClient):
        """Test loading a game that doesn't exist."""
        response = client.get("/api/v1/games/nonexistent-id/state")
        assert response.status_code == 404

class TestSettingsEndpoint:
    def test_get_settings_success(self, client: TestClient):
        """Test getting current settings."""
        response = client.get("/api/v1/settings")
        assert response.status_code == 200
        data = response.json()
        assert "settings" in data
        assert "message" in data
        message = data["message"].lower()
        assert "game" in message
        settings = data["settings"]
        assert "audio_volume" in settings
        assert "music_volume" in settings
        assert "sfx_volume" in settings
        assert "fullscreen" in settings

    def test_update_settings_success(self, client: TestClient):
        """Test updating settings."""
        response = client.post("/api/v1/settings", json={
            "settings": {
                "audio_volume": 80,
                "music_volume": 70,
                "sfx_volume": 90,
                "fullscreen": True
            }
        })
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "Settings updated successfully"
        assert "settings" in data
        settings = data["settings"]
        assert settings["audio_volume"] == 80
        assert settings["music_volume"] == 70
        assert settings["sfx_volume"] == 90
        assert settings["fullscreen"] is True

    def test_reset_settings(self, client: TestClient):
        """Test resetting settings to defaults."""
        response = client.get("/api/v1/settings/reset")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "Settings reset to defaults"
        assert "settings" in data
        settings = data["settings"]
        assert settings["audio_volume"] == 100
        assert settings["music_volume"] == 100
        assert settings["sfx_volume"] == 100
        assert settings["fullscreen"] is False

class TestExitGameEndpoint:
    def test_exit_game_without_save(self, client: TestClient):
        """Test exiting game without saving."""
        response = client.post("/api/v1/games/exit", json={"save_before_exit": False})
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Game exited without saving"
        assert not data["saved"]

    def test_exit_game_with_save(self, client: TestClient, test_game_id: str):
        """Test exiting game with save."""
        response = client.post("/api/v1/games/exit", json={
            "save_before_exit": True,
            "save_name": "Auto-Exit Save",
            "game_id": test_game_id
        })
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Game saved as 'Auto-Exit Save' before exit"
        assert data["saved"]
        assert "save_id" in data 