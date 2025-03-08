from sqlalchemy.orm import Session
from typing import Dict, List, Any, Optional

from app.database.repositories import GameRepository
from app.config import PlanetType, GalaxySize, Difficulty

def create_new_game(db: Session, player_name: str, difficulty: str = "normal", galaxy_size: str = "medium") -> dict:
    """
    Create a new game with the specified parameters using the repository pattern.
    """
    game_data = {
        "player_name": player_name,
        "difficulty": difficulty,
        "galaxy_size": galaxy_size,
        "player_resources": {
            "organic": 0,
            "mineral": 500,
            "energy": 200,
            "exotics": 0,
            "credits": 1000,
            "research": 0
        }
    }
    
    repo = GameRepository(db)
    game = repo.create_game(game_data)
    return game.to_dict()

def get_game(db: Session, game_id: str) -> Optional[dict]:
    """
    Get a game by ID.
    """
    repo = GameRepository(db)
    game = repo.get_game_by_id(game_id)
    if game:
        return game.to_dict()
    return None

def get_all_games(db: Session) -> List[dict]:
    """
    Get all games.
    """
    repo = GameRepository(db)
    games = repo.list_games()
    return [game.to_dict() for game in games]

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