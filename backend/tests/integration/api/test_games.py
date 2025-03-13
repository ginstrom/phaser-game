import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.utils.config_loader import config
from app.database.models import Base
from app.database.config import get_db
from app.utils.config_loader import GameSettings

# Use SQLite in-memory database for tests
TEST_DATABASE_URL = "sqlite:///:memory:"

# Create test engine
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

# Create test session factory
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Set up the test database with tables and any required initial data."""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Add any required initial data here
    db = TestingSessionLocal()
    try:
        # Add initial data if needed
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
    
    # Override the database dependency
    app.dependency_overrides[get_db] = override_get_db
    
    yield
    
    # Clean up after all tests
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def db():
    """Create a test database session."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_game_success(client: TestClient):
    """Test successful game creation with default settings."""
    response = client.post(
        "/api/v1/games/new",
        json={
            "player_name": "TestPlayer",
            "difficulty": "normal",
            "galaxy_size": "medium"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "game_id" in data
    assert "message" in data
    assert "initial_state" in data
    
    # Check message contains key information
    message = data["message"].lower()
    assert "testplayer" in message
    assert "normal" in message
    assert "medium" in message
    
    # Check initial state
    initial_state = data["initial_state"]
    assert "player" in initial_state
    assert initial_state["player"]["name"] == "TestPlayer"
    assert initial_state["difficulty"] == "normal"
    assert initial_state["galaxy"]["size"] == "medium"

def test_create_game_with_custom_settings(client: TestClient):
    """Test game creation with custom settings."""
    response = client.post(
        "/api/v1/games/new",
        json={
            "player_name": "CustomPlayer",
            "difficulty": "hard",
            "galaxy_size": "large",
            "num_computer_empires": 5,
            "player_perks": {
                "research_efficiency": 1.2,
                "combat_efficiency": 0.8,
                "economic_efficiency": 1.0,
                "diplomatic_influence": 1.0
            }
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "game_id" in data
    assert "message" in data
    assert "initial_state" in data
    
    initial_state = data["initial_state"]
    assert "player" in initial_state
    assert initial_state["player"]["name"] == "CustomPlayer"
    assert initial_state["difficulty"] == "hard"
    assert initial_state["galaxy"]["size"] == "large"

def test_create_game_invalid_difficulty(client: TestClient):
    """Test game creation with invalid difficulty."""
    response = client.post(
        "/api/v1/games/new",
        json={
            "player_name": "TestPlayer",
            "difficulty": "invalid_difficulty"
        }
    )
    assert response.status_code == 422  # Validation error

def test_create_game_invalid_galaxy_size(client: TestClient):
    """Test game creation with invalid galaxy size."""
    response = client.post(
        "/api/v1/games/new",
        json={
            "player_name": "TestPlayer",
            "galaxy_size": "invalid_size"
        }
    )
    assert response.status_code == 422  # Validation error

def test_create_game_missing_player_name(client: TestClient):
    """Test game creation without player name."""
    response = client.post(
        "/api/v1/games/new",
        json={
            "difficulty": "normal",
            "galaxy_size": "medium"
        }
    )
    assert response.status_code == 422  # Validation error 