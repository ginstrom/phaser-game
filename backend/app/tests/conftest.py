import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database.models import Base
from app.database.config import get_db

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
    
    # Override the database dependency
    app.dependency_overrides[get_db] = override_get_db
    
    yield
    
    # Clean up after all tests
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db_session: Session) -> TestClient:
    """Create a test client."""
    return TestClient(app)

@pytest.fixture
def db_session():
    """Create a test database session."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def sample_player():
    """Fixture providing sample player data."""
    return {
        "name": "TestPlayer",
        "empire": "Human Empire",
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
    """Fixture providing sample planet data."""
    return {
        "name": "Test Planet",
        "type": "terrestrial",
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
    """Fixture providing sample game state data."""
    return {
        "player": sample_player,
        "galaxy": {
            "size": "small",
            "systems": [],
            "explored_count": 0
        },
        "turn": 1,
        "difficulty": "normal"
    } 