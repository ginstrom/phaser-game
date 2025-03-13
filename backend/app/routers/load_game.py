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
from app.models.empire import EmpireResponse

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
    empires: List[EmpireResponse]

@router.get("/api/v1/games/saved", response_model=List[SavedGame])
def list_saved_games(db: Session = Depends(get_db)):
    """
    List all saved games.
    """
    games = get_all_games(db)
    # Convert to SavedGame format
    saved_games = []
    for game in games:
        saved_games.append({
            "game_id": game.id,
            "player_name": game.player_name,
            "empire_name": game.player_empire.name if game.player_empire else "Unknown",
            "turn": game.turn,
            "save_date": str(game.updated_at if hasattr(game, 'updated_at') else ""),
            "description": f"Turn {game.turn}"
        })
    return saved_games

@router.post("/api/v1/games/load", response_model=LoadGameResponse)
def load_game_endpoint(game_id: str, db: Session = Depends(get_db)):
    """
    Load a saved game with the specified game ID.
    """
    game = get_game(db, game_id)
    if not game:
        raise HTTPException(status_code=404, detail=f"Game with ID {game_id} not found")

    # Convert game model to response format
    return {
        "game_id": game.id,
        "message": "Game loaded successfully",
        "game_state": {
            "player": {
                "name": game.player_name,
                "empire": game.player_empire.to_dict() if game.player_empire else None,
                "resources": game.player_resources.to_dict() if game.player_resources else {}
            },
            "galaxy": game.galaxy.to_dict() if game.galaxy else {
                "size": game.galaxy_size,
                "systems": [],
                "explored_count": 0
            },
            "turn": game.turn,
            "difficulty": game.difficulty
        },
        "empires": [empire.to_dict() for empire in game.empires] if game.empires else []
    }