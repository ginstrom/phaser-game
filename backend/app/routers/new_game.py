"""Router for creating new game instances.
* Handles new game creation with configurable settings
* Validates player name, difficulty and galaxy size
* Returns initial game state and configuration
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field, constr
from typing import Dict, Any, Literal
from sqlalchemy.orm import Session

from app.database.config import get_db
from app.services.game_service import create_new_game

router = APIRouter()

class NewGameRequest(BaseModel):
    player_name: constr(min_length=1, max_length=50) = Field(..., description="Player name between 1 and 50 characters")
    difficulty: Literal["easy", "normal", "hard"] = Field(default="normal", description="Game difficulty level")
    galaxy_size: Literal["small", "medium", "large"] = Field(default="medium", description="Size of the galaxy")
    
class NewGameResponse(BaseModel):
    id: str
    game_id: str
    message: str
    initial_state: Dict[str, Any]

@router.post("/api/v1/games/new", response_model=NewGameResponse)
def create_new_game_endpoint(request: NewGameRequest, db: Session = Depends(get_db)):
    """
    Create a new game with the specified parameters.
    
    This endpoint creates a new game with the player name, difficulty, and galaxy size
    specified in the request. It returns the game ID, a success message, and the initial
    game state.
    """
    # Create a new game using the game service
    game = create_new_game(
        db=db,
        player_name=request.player_name,
        difficulty=request.difficulty,
        galaxy_size=request.galaxy_size
    )
    
    return {
        "id": game.id,  # Add id for test compatibility
        "game_id": game.id,
        "message": f"New game created for {request.player_name} with {request.difficulty} difficulty and {request.galaxy_size} galaxy size",
        "initial_state": game.to_dict()
    }