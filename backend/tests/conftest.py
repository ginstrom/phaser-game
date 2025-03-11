import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

# Set up config path to use actual project configs
os.environ["CONFIG_PATH"] = "/config"

# Now import the app and models after setting up config path
from app.database.config import Base, get_db
from app.database.models import Game, Galaxy, StarSystem, Planet, Empire, PlanetResources, PlayerResources
from app.main import app

# Configure in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

# Create engine with special SQLite settings for testing
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={
        "check_same_thread": False
    },
    poolclass=StaticPool,  # Use static pool to maintain connections
    echo=True
)

# Create session factory
TestSessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

@pytest.fixture(scope="function", autouse=True)
def setup_test_database():
    """Create tables before each test and drop them after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()

def override_get_db():
    """Override the database dependency for tests."""
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()

# Override the database dependency
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def client(setup_test_database):
    """Create a test client with a fresh database."""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def test_game(db_session):
    """Create a test game with basic setup."""
    game = Game(
        player_name="TestPlayer",
        empire_name="Test Empire",
        difficulty="normal",
        galaxy_size="medium"
    )
    db_session.add(game)
    
    # Create galaxy
    galaxy = Galaxy(game=game, size="medium")
    db_session.add(galaxy)
    
    # Create player empire
    empire = Empire(
        game=game,
        name="Test Empire",
        is_player=True,
        color="#FF0000",
        credits=1000,
        research_points=0
    )
    db_session.add(empire)
    
    # Create player resources
    resources = PlayerResources(
        game=game,
        mineral=500,
        energy=200,
        organic=0,
        exotics=0,
        credits=1000,
        research=0
    )
    db_session.add(resources)
    
    # Create a test star system
    system = StarSystem(
        galaxy=galaxy,
        name="Test System",
        position_x=0.0,
        position_y=0.0,
        explored=True,
        discovery_level=6
    )
    db_session.add(system)
    
    # Create test planets
    planet1 = Planet(
        system=system,
        name="Test Planet 1",
        type="terrestrial",
        size=5,
        colonized=False
    )
    planet2 = Planet(
        system=system,
        name="Test Planet 2",
        type="gas_giant",
        size=10,
        colonized=False
    )
    db_session.add_all([planet1, planet2])
    
    # Add resources to planets
    planet1_resources = PlanetResources(
        planet=planet1,
        organic=100,
        mineral=200,
        energy=150,
        exotics=50
    )
    planet2_resources = PlanetResources(
        planet=planet2,
        organic=50,
        mineral=300,
        energy=250,
        exotics=100
    )
    db_session.add_all([planet1_resources, planet2_resources])
    
    db_session.commit()
    return game

@pytest.fixture
def test_game_id(test_game):
    """Return the ID of the test game."""
    return test_game.id
