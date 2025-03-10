from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.empire import Empire, EmpireCreate, EmpireUpdate
from app.database.models import Game

def get_empire(db: Session, game_id: str, empire_id: str) -> Optional[Empire]:
    """Get a specific empire by ID."""
    return db.query(Empire).filter(
        Empire.game_id == game_id,
        Empire.id == empire_id
    ).first()

def get_empires(db: Session, game_id: str) -> List[Empire]:
    """Get all empires in a game."""
    return db.query(Empire).filter(Empire.game_id == game_id).all()

def create_empire(db: Session, game_id: str, empire_data: EmpireCreate) -> Empire:
    """Create a new empire in the game."""
    # Check if game exists
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise ValueError("Game not found")
    
    # Create empire
    empire = Empire(
        game_id=game_id,
        name=empire_data.name,
        color=empire_data.color,
        is_player=empire_data.is_player
    )
    
    db.add(empire)
    db.commit()
    db.refresh(empire)
    return empire

def update_empire(
    db: Session,
    game_id: str,
    empire_id: str,
    empire_update: EmpireUpdate
) -> Optional[Empire]:
    """Update an empire's details."""
    empire = get_empire(db, game_id, empire_id)
    if not empire:
        return None
    
    # Update fields if provided
    update_data = empire_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(empire, field, value)
    
    db.commit()
    db.refresh(empire)
    return empire

def delete_empire(db: Session, game_id: str, empire_id: str) -> bool:
    """Delete an empire from the game."""
    empire = get_empire(db, game_id, empire_id)
    if not empire:
        return False
    
    db.delete(empire)
    db.commit()
    return True

def initialize_game_empires(db: Session, game_id: str) -> List[Empire]:
    """Initialize the 4 empires for a new game, with one marked as player."""
    empires = [
        EmpireCreate(
            name="Human Empire",
            color="#4287f5",  # Blue
            is_player=True
        ),
        EmpireCreate(
            name="Zylaxian Collective",
            color="#f54242",  # Red
            is_player=False
        ),
        EmpireCreate(
            name="Verdant Conclave",
            color="#42f54e",  # Green
            is_player=False
        ),
        EmpireCreate(
            name="Stellar Dynasty",
            color="#f5d442",  # Yellow
            is_player=False
        )
    ]
    
    created_empires = []
    for empire_data in empires:
        empire = create_empire(db, game_id, empire_data)
        created_empires.append(empire)
    
    return created_empires 