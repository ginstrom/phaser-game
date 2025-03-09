from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List, Any, Optional

from app.database.repositories import GameRepository

async def create_new_game(
    db: AsyncSession, 
    player_name: str, 
    difficulty: str = "normal", 
    galaxy_size: str = "medium"
) -> dict:
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
    game = await repo.create_game(game_data)
    return game.to_dict()

async def get_game(db: AsyncSession, game_id: str) -> Optional[dict]:
    """
    Get a game by ID.
    """
    repo = GameRepository(db)
    game = await repo.get_game_by_id(game_id)
    if game:
        return game.to_dict()
    return None

async def get_all_games(db: AsyncSession) -> List[dict]:
    """
    Get all games.
    """
    repo = GameRepository(db)
    games = await repo.list_games()
    return [game.to_dict() for game in games]

async def delete_game(db: AsyncSession, game_id: str) -> bool:
    """
    Delete a game by ID.
    """
    repo = GameRepository(db)
    return await repo.delete_game(game_id)

async def update_game_turn(db: AsyncSession, game_id: str, turn: int) -> bool:
    """
    Update the turn of a game.
    """
    repo = GameRepository(db)
    return await repo.update_game_turn(game_id, turn)