from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter()

class NewGameRequest(BaseModel):
    player_name: str
    difficulty: str = "normal"
    galaxy_size: str = "medium"
    
class NewGameResponse(BaseModel):
    game_id: str
    message: str
    initial_state: Dict[str, Any]

@router.post("/new-game", response_model=NewGameResponse)
async def create_new_game(request: NewGameRequest):
    """
    Create a new game with the specified parameters.
    
    This is a stub endpoint that will be implemented with actual game creation logic in the future.
    """
    try:
        # Stub implementation - in a real implementation, this would create a new game
        # and return the initial game state
        return {
            "game_id": "game-12345",
            "message": f"New game created for {request.player_name} with {request.difficulty} difficulty and {request.galaxy_size} galaxy size",
            "initial_state": {
                "player": {
                    "name": request.player_name,
                    "empire": "Human Empire",
                    "resources": {
                        "credits": 1000,
                        "minerals": 500,
                        "energy": 200
                    }
                },
                "galaxy": {
                    "size": request.galaxy_size,
                    "systems": 10,  # This would be determined by galaxy size in a real implementation
                    "explored": 1
                },
                "turn": 1
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create new game: {str(e)}")
