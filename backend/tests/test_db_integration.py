import pytest
from sqlalchemy.orm import Session

from app.database.repositories import GameRepository
from app.database.models import Game, Galaxy, StarSystem, Planet, PlanetResources, PlayerResources

def test_create_game(db: Session):
    """Test creating a game in the database."""
    # Prepare test data
    game_data = {
        "player_name": "TestPlayer",
        "difficulty": "normal",
        "galaxy_size": "small",
        "player_resources": {
            "organic": 0,
            "mineral": 500,
            "energy": 200,
            "credits": 1000
        }
    }
    
    # Create repository and game
    repo = GameRepository(db)
    game = repo.create_game(game_data)
    
    # Verify game was created
    assert game is not None
    assert game.id is not None
    assert game.player_name == "TestPlayer"
    assert game.difficulty == "normal"
    assert game.galaxy_size == "small"
    
    # Verify player resources were created
    assert game.player_resources is not None
    assert game.player_resources.mineral == 500
    assert game.player_resources.energy == 200
    assert game.player_resources.credits == 1000
    
    # Verify galaxy was created
    assert game.galaxy is not None
    assert game.galaxy.size == "small"
    
    # Verify star systems were created
    assert len(game.galaxy.systems) > 0
    
    # Verify first system is explored
    assert game.galaxy.systems[0].explored is True
    assert game.galaxy.systems[0].discovery_level == 6  # visited
    assert game.galaxy.explored_count == 1
    
    # Verify planets were created
    first_system = game.galaxy.systems[0]
    assert len(first_system.planets) > 0
    
    # Verify planet resources were created
    first_planet = first_system.planets[0]
    assert first_planet.resources is not None

def test_get_game_by_id(db: Session):
    """Test retrieving a game by ID."""
    # First create a game
    repo = GameRepository(db)
    game = repo.create_game({"player_name": "TestPlayer"})
    game_id = game.id
    
    # Now retrieve it
    retrieved_game = repo.get_game_by_id(game_id)
    
    # Verify it's the same game
    assert retrieved_game is not None
    assert retrieved_game.id == game_id
    assert retrieved_game.player_name == "TestPlayer"

def test_list_games(db: Session):
    """Test listing all games."""
    # Create repository
    repo = GameRepository(db)
    
    # Create some games
    game1 = repo.create_game({"player_name": "Player1"})
    game2 = repo.create_game({"player_name": "Player2"})
    
    # List games
    games = repo.list_games()
    
    # Verify both games are in the list
    assert len(games) >= 2
    game_ids = [game.id for game in games]
    assert game1.id in game_ids
    assert game2.id in game_ids

def test_delete_game(db: Session):
    """Test deleting a game."""
    # First create a game
    repo = GameRepository(db)
    game = repo.create_game({"player_name": "TestPlayer"})
    game_id = game.id
    
    # Now delete it
    result = repo.delete_game(game_id)
    
    # Verify it was deleted
    assert result is True
    
    # Try to retrieve it
    deleted_game = repo.get_game_by_id(game_id)
    
    # Verify it's not found
    assert deleted_game is None

def test_update_game_turn(db: Session):
    """Test updating a game's turn."""
    # First create a game
    repo = GameRepository(db)
    game = repo.create_game({"player_name": "TestPlayer"})
    game_id = game.id
    
    # Verify initial turn
    assert game.turn == 1
    
    # Update turn
    result = repo.update_game_turn(game_id, 5)
    
    # Verify update was successful
    assert result is True
    
    # Retrieve updated game
    updated_game = repo.get_game_by_id(game_id)
    
    # Verify turn was updated
    assert updated_game.turn == 5