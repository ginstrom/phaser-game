from sqlalchemy.orm import Session
from typing import Dict, List, Any, Optional

from app.database.repositories import GameRepository
from app.models.game import GameCreate
from app.database.models import Game
from app.services.empire_service import initialize_game_empires

def create_new_game(
    db: Session,
    player_name: str,
    difficulty: str = "normal",
    galaxy_size: str = "medium",
    num_computer_empires: Optional[int] = None,
    player_perks: Optional[Dict] = None
) -> Game:
    """Create a new game with the specified settings."""
    game_data = GameCreate(
        player_name=player_name,
        difficulty=difficulty,
        galaxy_size=galaxy_size
    )
    repo = GameRepository(db)
    game = repo.create_game(game_data)
    
    # Initialize empires
    empires = initialize_game_empires(
        db=db,
        game_id=game.id,
        player_name=player_name,
        num_computer_empires=num_computer_empires,
        difficulty=difficulty,
        player_perks=player_perks
    )
    
    # Update player_empire_id in game
    player_empire = next(empire for empire in empires if empire.is_player)
    game.player_empire_id = player_empire.id
    db.commit()
    
    return game

def get_game(db: Session, game_id: str) -> Optional[Game]:
    """Get a game by ID."""
    return db.query(Game).filter(Game.id == game_id).first()

def get_all_games(db: Session) -> List[Game]:
    """
    Get all games.
    """
    repo = GameRepository(db)
    return repo.list_games()

def delete_game(db: Session, game_id: str) -> bool:
    """
    Delete a game by ID.
    """
    repo = GameRepository(db)
    return repo.delete_game(game_id)

def update_game_turn(db: Session, game_id: str, turn: int) -> bool:
    """
    Update the turn of a game.
    """
    repo = GameRepository(db)
    return repo.update_game_turn(game_id, turn)

def create_game(db: Session, game_data: GameCreate) -> Game:
    """Create a new game."""
    game = Game(
        player_name=game_data.player_name,
        difficulty=game_data.difficulty,
        galaxy_size=game_data.galaxy_size,
        turn=1
    )
    
    db.add(game)
    db.commit()
    db.refresh(game)
    return game