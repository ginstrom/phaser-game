from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.database.config import get_db
from app.database.models import GameStateDB
from app.models.game import GameState, Player, Galaxy
from app.config import GalaxySize, Difficulty

router = APIRouter()

@router.post("/new-game")
def create_new_game(
    player_name: str,
    galaxy_size: GalaxySize = GalaxySize.MEDIUM,
    difficulty: Difficulty = Difficulty.NORMAL,
    db: Session = Depends(get_db)
):
    # Create new game state
    game_state = GameState(
        id=str(uuid.uuid4()),
        player=Player(name=player_name),
        galaxy=Galaxy(size=galaxy_size),
        difficulty=difficulty
    )
    
    # Create database record
    db_game = GameStateDB(
        id=game_state.id,
        player_name=game_state.player.name,
        empire_name=game_state.player.empire,
        turn=game_state.turn,
        difficulty=game_state.difficulty.value,
        game_data=game_state.to_dict()
    )
    
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    
    return {
        "game_id": db_game.id,
        "message": "Game created successfully",
        "initial_state": db_game.game_data
    }

@router.get("/saved-games", response_model=List[dict])
def list_saved_games(db: Session = Depends(get_db)):
    games = db.query(GameStateDB).all()
    return [game.to_dict() for game in games]

@router.post("/load-game")
def load_game(game_id: str, db: Session = Depends(get_db)):
    game = db.query(GameStateDB).filter(GameStateDB.id == game_id).first()
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game with ID {game_id} not found"
        )
    
    return {
        "game_id": game.id,
        "message": "Game loaded successfully",
        "game_state": game.game_data
    } 