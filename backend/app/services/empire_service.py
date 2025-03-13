from sqlalchemy.orm import Session
from typing import List, Optional, Dict
import random

from app.models.empire import EmpireDB, EmpireCreate, EmpireUpdate, EmpireResponse
from app.database.models import Game
from app.utils.name_generator import generate_empire_name
from app.utils.config_loader import config

def get_empire(db: Session, game_id: str, empire_id: str) -> Optional[EmpireResponse]:
    """Get a specific empire by ID."""
    empire_db = db.query(EmpireDB).filter(
        EmpireDB.game_id == game_id,
        EmpireDB.id == empire_id
    ).first()
    return empire_db.to_api_model() if empire_db else None

def get_empires(db: Session, game_id: str) -> List[EmpireResponse]:
    """Get all empires in a game."""
    empire_dbs = db.query(EmpireDB).filter(EmpireDB.game_id == game_id).all()
    return [empire_db.to_api_model() for empire_db in empire_dbs]

def create_empire(db: Session, game_id: str, empire_data: EmpireCreate) -> EmpireResponse:
    """Create a new empire in the game."""
    # Check if game exists
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise ValueError("Game not found")
    
    # Create empire
    empire_db = EmpireDB(
        game_id=game_id,
        name=empire_data.name,
        color=empire_data.color,
        is_player=empire_data.is_player
    )
    
    db.add(empire_db)
    db.commit()
    db.refresh(empire_db)
    return empire_db.to_api_model()

def update_empire(
    db: Session,
    game_id: str,
    empire_id: str,
    empire_update: EmpireUpdate
) -> Optional[EmpireResponse]:
    """Update an empire's details."""
    empire_db = db.query(EmpireDB).filter(
        EmpireDB.game_id == game_id,
        EmpireDB.id == empire_id
    ).first()
    if not empire_db:
        return None
    
    # Update fields if provided
    update_data = empire_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(empire_db, field, value)
    
    db.commit()
    db.refresh(empire_db)
    return empire_db.to_api_model()

def delete_empire(db: Session, game_id: str, empire_id: str) -> bool:
    """Delete an empire from the game."""
    empire_db = db.query(EmpireDB).filter(
        EmpireDB.game_id == game_id,
        EmpireDB.id == empire_id
    ).first()
    if not empire_db:
        return False
    
    db.delete(empire_db)
    db.commit()
    return True

def create_player_empire(
    db: Session,
    game_id: str,
    name: str,
    perks: Optional[Dict] = None,
    difficulty: str = "normal"
) -> EmpireResponse:
    """Create a new player empire with specified perks and starting resources."""
    if perks is None:
        perks = config.get_config_section("defaults", "perks").model_dump()

    starting_resources = config.get_config_section("defaults", "starting_resources")
    if isinstance(starting_resources, dict):
        resources = starting_resources[difficulty]
    else:
        resources = getattr(starting_resources, difficulty)

    empire_db = EmpireDB(
        game_id=game_id,
        name=name,
        is_player=True,
        color="#00FF00",  # Default player color (green)
        credits=resources.credits,
        research_points=resources.research_points,
        perks=perks
    )

    db.add(empire_db)
    db.commit()
    db.refresh(empire_db)

    return empire_db.to_api_model()

def create_computer_empire(
    db: Session,
    game_id: str,
    archetype_index: int = 0,
    difficulty: str = "normal"
) -> EmpireResponse:
    """Create a new computer empire with specified archetype and difficulty."""
    archetypes = config.get_config_section("empire_archetypes")
    archetype = archetypes[archetype_index]
    
    # Get existing empire colors for this game
    existing_colors = [color[0] for color in 
        db.query(EmpireDB.color)
        .filter(EmpireDB.game_id == game_id)
        .all()
    ]
    
    # Find a unique color from the archetype's color range
    available_colors = [c for c in archetype.color_range if c not in existing_colors]
    if not available_colors:
        # If all colors are taken, generate a new one by slightly modifying an existing one
        base_color = random.choice(archetype.color_range)
        color = f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"
    else:
        color = random.choice(available_colors)
    
    perks = archetype.perks.model_dump()

    # Get existing empire count for this archetype to make name unique
    existing_count = db.query(EmpireDB).filter(
        EmpireDB.game_id == game_id,
        EmpireDB.name.like(f"{archetype.name} Empire%")
    ).count()

    empire_name = f"{archetype.name} Empire {existing_count + 1}" if existing_count > 0 else f"{archetype.name} Empire"

    starting_resources = config.get_config_section("defaults", "starting_resources")
    base_resources = starting_resources["normal"]  # Always use normal as base for computer empires

    # Apply difficulty bonuses for computer empires
    if difficulty == "hard":
        credits = int(base_resources.credits * 1.5)
        research_points = int(base_resources.research_points * 1.5)
    elif difficulty == "easy":
        credits = int(base_resources.credits * 0.75)
        research_points = int(base_resources.research_points * 0.75)
    else:
        credits = base_resources.credits
        research_points = base_resources.research_points

    empire_db = EmpireDB(
        game_id=game_id,
        name=empire_name,
        is_player=False,
        color=color,
        credits=credits,
        research_points=research_points,
        perks=perks
    )

    db.add(empire_db)
    db.commit()
    db.refresh(empire_db)

    return empire_db.to_api_model()

def initialize_game_empires(
    db: Session,
    game_id: str,
    player_name: str,
    num_computer_empires: Optional[int] = None,
    difficulty: str = "normal",
    player_perks: Optional[Dict] = None
) -> List[EmpireResponse]:
    """Initialize all empires for a new game."""
    game_settings = config.get_config_section("game_settings")
    
    if num_computer_empires is None:
        num_computer_empires = game_settings.default_computer_empires
    else:
        # Validate number of computer empires
        if not (game_settings.min_computer_empires <= num_computer_empires <= game_settings.max_computer_empires):
            raise ValueError(
                f"Number of computer empires must be between "
                f"{game_settings.min_computer_empires} and {game_settings.max_computer_empires}"
            )
    
    empires = []
    
    # Create player empire
    player_empire = create_player_empire(
        db=db,
        game_id=game_id,
        name=f"{player_name}'s Empire",
        perks=player_perks,
        difficulty=difficulty
    )
    empires.append(player_empire)
    
    # Create computer empires
    for _ in range(num_computer_empires):
        computer_empire = create_computer_empire(
            db=db,
            game_id=game_id,
            difficulty=difficulty
        )
        empires.append(computer_empire)
    
    return empires 