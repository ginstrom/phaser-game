import pytest
from typing import Generator, Dict, Any
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database.models import Base, Game, EmpireDB, PlayerResources, Galaxy
from app.database.config import get_db

# Global variables for test database
TEST_DATABASE_URL = "sqlite:///:memory:"
TEST_ENGINE = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=TEST_ENGINE)

# Cache for test_client instances
_test_client_cache: Dict[str, TestClient] = {}

# Set up base tables once for all tests
Base.metadata.create_all(bind=TEST_ENGINE)

@pytest.fixture(scope="session")
def engine():
    """Return the test database engine."""
    return TEST_ENGINE

@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """
    Creates a fresh database session for each test function.
    Uses a transaction that is rolled back after the test.
    """
    connection = TEST_ENGINE.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        # Roll back the transaction to reset DB state
        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture
def client(db_session: Session) -> TestClient:
    """
    Create a test client using a session-specific DB dependency override.
    """
    def _get_test_db():
        try:
            yield db_session
        finally:
            pass  # db_session is handled by the fixture

    # Use a fresh copy of the app for each client instance
    test_app = app
    test_app.dependency_overrides[get_db] = _get_test_db
    
    # Use cached client if available by session_id
    session_id = id(db_session)
    if session_id not in _test_client_cache:
        _test_client_cache[session_id] = TestClient(test_app)
    
    client = _test_client_cache[session_id]
    yield client
    
    # Clean up after test
    test_app.dependency_overrides.clear()
    if session_id in _test_client_cache:
        del _test_client_cache[session_id]

@pytest.fixture
def test_game_data() -> Dict[str, Any]:
    """Test data for game creation."""
    return {
        "player_name": "TestPlayer",
        "difficulty": "normal",
        "galaxy_size": "medium"
    }

@pytest.fixture
def test_player_name() -> str:
    """A test player name."""
    return "TestPlayer"

@pytest.fixture
def test_game(db_session: Session) -> Game:
    """Create a test game with proper initialization."""
    # Create game
    game = Game(
        player_name="TestPlayer",
        difficulty="normal",
        galaxy_size="medium"
    )
    
    # Create player empire
    empire = EmpireDB(
        game=game,
        name="TestPlayer's Empire",
        is_player=True,
        color="#0000FF"
    )
    
    # Create player resources
    resources = PlayerResources(
        game=game,
        organic=100,
        mineral=100,
        energy=100,
        exotics=0,
        credits=1000,
        research=0
    )
    
    # Create galaxy
    galaxy = Galaxy(
        game=game,
        size="medium",
        total_systems=100,
        explored_count=0
    )
    
    # Set relationships
    game.player_empire = empire
    game.player_resources = resources
    game.galaxy = galaxy
    
    db_session.add(game)
    db_session.add(empire)
    db_session.add(resources)
    db_session.add(galaxy)
    db_session.commit()
    db_session.refresh(game)
    return game

@pytest.fixture
def test_game_id(test_game: Game) -> str:
    """Get the ID of the test game."""
    return test_game.id

# Clean up tables after all tests are complete
@pytest.fixture(scope="session", autouse=True)
def cleanup_database():
    """Clean up the database after all tests are complete."""
    yield
    Base.metadata.drop_all(bind=TEST_ENGINE) 