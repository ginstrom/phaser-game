import pytest
from fastapi.testclient import TestClient
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

# Add the backend directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Set test environment
os.environ["ENVIRONMENT"] = "test"

from app.main import app
from app.database.models import Base, Game
from app.models.empire import Empire
from app.database.config import get_db

# Use SQLite in-memory database for tests
TEST_DATABASE_URL = "sqlite:///:memory:"

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Create test engine
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

# Create test session factory
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables
Base.metadata.create_all(bind=engine)

# Override the database dependency
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)

@pytest.fixture
def db():
    """Create a test database session."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def test_game(db):
    """Create a test game."""
    game = Game(
        player_name="TestPlayer",
        difficulty="normal",
        galaxy_size="medium"
    )
    db.add(game)
    db.commit()
    db.refresh(game)
    return game

@pytest.fixture
def test_game_id(test_game):
    """Return the ID of the test game."""
    return test_game.id

# Tests
def test_root_endpoint(client):
    """Test the root endpoint returns correct welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to the 4X Space Empire API"
    assert data["version"] == "0.1.0"
    assert data["documentation"] == "/docs"

class TestNewGameEndpoint:
    def test_create_new_game_success(self, client):
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

    def test_create_new_game_invalid_data(self, client):
        """Test creating a new game with invalid parameters."""
        response = client.post("/api/v1/games/new", json={
            "player_name": "",  # Empty name should be invalid
            "galaxy_size": "invalid",  # Invalid size
            "difficulty": "invalid"  # Invalid difficulty
        })
        assert response.status_code == 422

class TestLoadGameEndpoint:
    def test_load_game_success(self, client, test_game_id):
        """Test loading an existing game."""
        # First create a game
        create_response = client.post(
            "/api/v1/games/new",
            json={
                "player_name": "TestPlayer",
                "difficulty": "normal",
                "galaxy_size": "medium"
            }
        )
        assert create_response.status_code == 200
        game_data = create_response.json()
        game_id = game_data["id"]

        # Then try to load it
        response = client.post(f"/api/v1/games/load?game_id={game_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["game_id"] == game_id
        assert "game_state" in data
        assert "empires" in data

    def test_load_nonexistent_game(self, client):
        """Test loading a game that doesn't exist."""
        response = client.post("/load-game", json={"game_id": "nonexistent-id"})
        assert response.status_code == 404

class TestSettingsEndpoint:
    def test_get_settings_success(self, client):
        """Test getting current settings."""
        response = client.get("/settings")
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

    def test_update_settings_success(self, client):
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

    def test_reset_settings(self, client):
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
    def test_exit_game_without_save(self, client):
        """Test exiting game without saving."""
        response = client.post("/exit", json={"save_before_exit": False})
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Game exited without saving"
        assert not data["saved"]

    def test_exit_game_with_save(self, client, test_game_id):
        """Test exiting game with save."""
        response = client.post("/exit", json={
            "save_before_exit": True,
            "save_name": "Auto-Exit Save"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Game saved as 'Auto-Exit Save' before exit"
        assert data["saved"]
        assert "save_id" in data 