import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint returns correct welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to the 4X Space Empire API"
    assert data["version"] == "0.1.0"
    assert data["documentation"] == "/docs"

class TestNewGameEndpoint:
    def test_create_new_game_success(self):
        """Test creating a new game with valid parameters."""
        response = client.post("/new-game", json={
            "player_name": "TestPlayer",
            "galaxy_size": "medium",
            "difficulty": "normal"
        })
        assert response.status_code == 200
        data = response.json()
        assert "game_id" in data
        assert "message" in data
        assert "TestPlayer" in data["message"]
        assert "normal" in data["message"]
        assert "medium" in data["message"]
        assert "initial_state" in data

    def test_create_new_game_invalid_data(self):
        """Test creating a new game with invalid parameters."""
        response = client.post("/new-game", json={
            "player_name": "",  # Empty name should be invalid
            "galaxy_size": "invalid",  # Invalid size
            "difficulty": "invalid"  # Invalid difficulty
        })
        assert response.status_code == 422

class TestLoadGameEndpoint:
    def test_load_game_success(self, test_game_id):
        """Test loading an existing game."""
        response = client.post("/load-game", json={"game_id": test_game_id})
        assert response.status_code == 200
        data = response.json()
        assert data["game_id"] == test_game_id
        assert data["message"] == "Game loaded successfully"
        assert "game_state" in data

    def test_load_nonexistent_game(self):
        """Test loading a game that doesn't exist."""
        response = client.post("/load-game", json={"game_id": "nonexistent-id"})
        assert response.status_code == 404

class TestSettingsEndpoint:
    def test_get_settings_success(self):
        """Test getting current settings."""
        response = client.get("/settings")
        assert response.status_code == 200
        data = response.json()
        assert "settings" in data
        assert "message" in data
        assert data["message"] == "Settings retrieved successfully"

    def test_update_settings_success(self):
        """Test updating settings."""
        response = client.post("/settings", json={
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

    def test_reset_settings(self):
        """Test resetting settings to defaults."""
        response = client.get("/settings/reset")
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
    def test_exit_game_without_save(self):
        """Test exiting game without saving."""
        response = client.post("/exit", json={"save_before_exit": False})
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Game exited without saving"
        assert data["saved"] is False

    def test_exit_game_with_save(self, test_game_id):
        """Test exiting game with save."""
        response = client.post("/exit", json={
            "save_before_exit": True,
            "save_name": "Auto-Exit Save"
        })
        assert response.status_code == 200
        data = response.json()
        assert "Game saved as 'Auto-Exit Save' before exit" in data["message"]
        assert data["saved"] is True
        assert "save_id" in data 