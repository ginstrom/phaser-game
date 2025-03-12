"""Router for managing saved game operations.
* Lists available saved games with metadata
* Handles loading saved game states
* Returns complete game state for resuming play
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from app.database.config import get_db
from app.services.game_service import get_game, get_all_games

router = APIRouter()

class SavedGame(BaseModel):
    game_id: str
    player_name: str
    empire_name: str
    turn: int
    save_date: str
    description: Optional[str] = None

class LoadGameRequest(BaseModel):
    game_id: str

class LoadGameResponse(BaseModel):
    game_id: str
    message: str
    game_state: Dict[str, Any]

@router.get("/saved-games", response_model=List[SavedGame])
def list_saved_games(db: Session = Depends(get_db)):
    """
    List all saved games.
    """
    games = get_all_games(db)
    # Convert to SavedGame format
    saved_games = []
    for game in games:
        saved_games.append({
            "game_id": game["id"],
            "player_name": game["player"]["name"],
            "empire_name": game["player"]["empire"],
            "turn": game["turn"],
            "save_date": str(game.get("updated_at", "")),
            "description": f"Turn {game['turn']}"
        })
    return saved_games

@router.post("/load-game", response_model=LoadGameResponse)
def load_game_endpoint(request: LoadGameRequest, db: Session = Depends(get_db)):
    """
    Load a saved game with the specified game ID.
    """
    game = get_game(db, request.game_id)
    if not game:
        raise HTTPException(status_code=404, detail=f"Game with ID {request.game_id} not found")
    
    # Ensure the game_id is at the top level for API compatibility
    return {
        "game_id": game["id"],
        "message": "Game loaded successfully",
        "game_state": {
            "player": game["player"],
            "galaxy": game["galaxy"],
            "turn": game["turn"],
            "difficulty": game["difficulty"]
        }
    }