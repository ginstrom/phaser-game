from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional, Dict
import json
import os

from app.database.config import get_db
from app.models.game import GameCreate, GameResponse
from app.services.game_service import create_game
from app.services.empire_service import initialize_game_empires

router = APIRouter(prefix="/api/v1")

def load_game_config():
    """Load game configuration from JSON file."""
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'config', 'game_config.json')
    with open(config_path) as f:
        return json.load(f)

@router.post("/games/new", response_model=GameResponse)
async def create_new_game(
    request_data: dict,
    db: Session = Depends(get_db)
):
    """Create a new game with empires."""
    # Load game configuration
    game_config = load_game_config()
    min_empires = game_config["game_settings"]["min_computer_empires"]
    max_empires = game_config["game_settings"]["max_computer_empires"]
    default_empires = game_config["game_settings"]["default_computer_empires"]
    
    # Extract data from request
    player_name = request_data.get("player_name")
    if not player_name:
        raise HTTPException(status_code=422, detail="player_name is required")
    
    difficulty = request_data.get("difficulty", "normal")
    galaxy_size = request_data.get("galaxy_size", "medium")
    player_perks = request_data.get("player_perks")
    
    # Handle num_computer_empires
    num_computer_empires = request_data.get("num_computer_empires")
    if num_computer_empires is not None:
        try:
            num_computer_empires = float(num_computer_empires)  # Convert to float first to handle decimals
            if not num_computer_empires.is_integer():
                raise ValueError("Must be an integer")
            num_computer_empires = int(num_computer_empires)
            if num_computer_empires < min_empires:
                raise HTTPException(
                    status_code=422,
                    detail=f"Number of computer empires must be at least {min_empires}"
                )
            if num_computer_empires > max_empires:
                raise HTTPException(
                    status_code=422,
                    detail=f"Number of computer empires must be at most {max_empires}"
                )
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=422,
                detail=f"Invalid value for num_computer_empires. Must be an integer between {min_empires} and {max_empires}"
            )
    else:
        num_computer_empires = default_empires
    
    # Create game data
    game_data = GameCreate(
        player_name=player_name,
        difficulty=difficulty,
        galaxy_size=galaxy_size
    )
    
    # Create the game first
    game = create_game(db=db, game_data=game_data)
    
    try:
        # Initialize empires
        empires = initialize_game_empires(
            db=db,
            game_id=game.id,
            player_name=game_data.player_name,
            num_computer_empires=num_computer_empires,
            difficulty=game_data.difficulty,
            player_perks=player_perks
        )
        
        # Update player_empire_id in game
        player_empire = next(empire for empire in empires if empire.is_player)
        game.player_empire_id = player_empire.id
        db.commit()
        
        return game
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e)) 