from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.config import get_db
from app.models.empire import EmpireCreate, EmpireUpdate, EmpireResponse
from app.services.empire_service import (
    get_empire,
    get_empires,
    create_empire,
    update_empire,
    delete_empire
)

router = APIRouter()

@router.get("/games/{game_id}/empires", response_model=List[EmpireResponse])
async def list_empires(
    game_id: str,
    db: Session = Depends(get_db)
):
    """Get all empires in a game."""
    return get_empires(db, game_id)

@router.get("/games/{game_id}/empires/{empire_id}", response_model=EmpireResponse)
async def get_empire_details(
    game_id: str,
    empire_id: str,
    db: Session = Depends(get_db)
):
    """Get details of a specific empire."""
    empire = get_empire(db, game_id, empire_id)
    if not empire:
        raise HTTPException(status_code=404, detail="Empire not found")
    return empire

@router.post("/games/{game_id}/empires", response_model=EmpireResponse)
async def create_new_empire(
    game_id: str,
    empire: EmpireCreate,
    db: Session = Depends(get_db)
):
    """Create a new empire in the game."""
    return create_empire(db, game_id, empire)

@router.patch("/games/{game_id}/empires/{empire_id}", response_model=EmpireResponse)
async def update_empire_details(
    game_id: str,
    empire_id: str,
    empire_update: EmpireUpdate,
    db: Session = Depends(get_db)
):
    """Update an empire's details."""
    empire = update_empire(db, game_id, empire_id, empire_update)
    if not empire:
        raise HTTPException(status_code=404, detail="Empire not found")
    return empire

@router.delete("/games/{game_id}/empires/{empire_id}")
async def delete_empire_endpoint(
    game_id: str,
    empire_id: str,
    db: Session = Depends(get_db)
):
    """Delete an empire from the game."""
    success = delete_empire(db, game_id, empire_id)
    if not success:
        raise HTTPException(status_code=404, detail="Empire not found")
    return {"message": "Empire deleted successfully"} 