from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession
from app.database.config import get_db
from app.config import Difficulty, GalaxySize
from app.services.game_service import create_new_game

router = APIRouter()

class NewGameRequest(BaseModel):
    player_name: str
    difficulty: str = "normal"  # Kept as string for API compatibility
    galaxy_size: str = "medium"  # Kept as string for API compatibility
    
class NewGameResponse(BaseModel):
    game_id: str
    message: str
    initial_state: Dict[str, Any]

@router.post("/new-game", response_model=NewGameResponse)
async def create_new_game_endpoint(request: NewGameRequest, db: AsyncSession = Depends(get_db)):
    """
    Create a new game with the specified parameters.
    
    This endpoint creates a new game with the player name, difficulty, and galaxy size
    specified in the request. It returns the game ID, a success message, and the initial
    game state.
    """
    try:
        # Create a new game using the game service
        game = await create_new_game(db,
            player_name=request.player_name,
            difficulty=request.difficulty,
            galaxy_size=request.galaxy_size
        )
        
        return {
            "game_id": game["id"],
            "message": f"New game created for {request.player_name} with {request.difficulty} difficulty and {request.galaxy_size} galaxy size",
            "initial_state": game
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create new game: {str(e)}")
