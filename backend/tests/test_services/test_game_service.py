import pytest
from sqlalchemy.orm import Session

from app.services.game_service import create_game, get_game
from app.models.game import GameCreate
from app.database.models import Game

@pytest.fixture
def test_game_data() -> GameCreate:
    return GameCreate(
        player_name="TestPlayer",
        difficulty="normal",
        galaxy_size="medium"
    )

@pytest.fixture
def db(db_session: Session) -> Session:
    """Provide a database session for testing."""
    return db_session

def test_create_game(db: Session, test_game_data: GameCreate):
    """Test creating a new game."""
    game = create_game(db=db, game_data=test_game_data)
    
    assert game is not None
    assert isinstance(game, Game)
    assert game.player_name == test_game_data.player_name
    assert game.difficulty == test_game_data.difficulty
    assert game.galaxy_size == test_game_data.galaxy_size
    assert game.turn == 1

def test_create_game_with_custom_settings(db: Session):
    """Test creating a game with custom settings."""
    game_data = GameCreate(
        player_name="CustomPlayer",
        difficulty="hard",
        galaxy_size="large"
    )
    
    game = create_game(db=db, game_data=game_data)
    
    assert game.player_name == "CustomPlayer"
    assert game.difficulty == "hard"
    assert game.galaxy_size == "large"
    assert game.turn == 1

def test_get_game(db: Session, test_game_data: GameCreate):
    """Test retrieving a game by ID."""
    # Create a game first
    created_game = create_game(db=db, game_data=test_game_data)
    
    # Retrieve the game
    retrieved_game = get_game(db, created_game.id)
    
    assert retrieved_game is not None
    assert retrieved_game.id == created_game.id
    assert retrieved_game.player_name == test_game_data.player_name
    assert retrieved_game.difficulty == test_game_data.difficulty
    assert retrieved_game.galaxy_size == test_game_data.galaxy_size

def test_get_nonexistent_game(db: Session):
    """Test retrieving a game that doesn't exist."""
    game = get_game(db, "nonexistent-id")
    assert game is None 