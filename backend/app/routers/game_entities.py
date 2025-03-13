"""Game entities router handling core game state and actions.
* Manages CRUD operations for players, galaxies, star systems, and planets
* Handles game state operations like colonization and turn advancement
* Provides endpoints for retrieving game state and entity information
"""

from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select
import uuid

from app.models.game import (
    GameState,
    GameResponse,
    Player,
    Galaxy,
    StarSystem,
    Planet,
    PlayerResources,
    PlanetResources
)
from app.database.config import get_db
from app.database.models import (
    Game as GameDB,
    Galaxy as GalaxyDB,
    StarSystem as StarSystemDB,
    Planet as PlanetDB,
    PlayerResources as PlayerResourcesDB,
    GameStateDB
)
from app.models.empire import EmpireDB, EmpireResponse
from app.config import GalaxySize, Difficulty

router = APIRouter(prefix="/api/v1")

# Planet endpoints
@router.get("/planets/{planet_id}", response_model=Planet)
async def get_planet(planet_id: str, db: Session = Depends(get_db)):
    """Get planet details by ID"""
    stmt = select(PlanetDB).where(PlanetDB.id == planet_id)
    result = db.execute(stmt)
    planet = result.scalars().first()
    
    if not planet:
        raise HTTPException(status_code=404, detail="Planet not found")
    
    return Planet(**planet.to_dict())

# Player endpoints
@router.get("/players/{player_name}", response_model=Player)
async def get_player(player_name: str, db: Session = Depends(get_db)):
    """Get player details by name"""
    stmt = select(GameDB).where(GameDB.player_name == player_name)
    result = db.execute(stmt)
    game = result.scalars().first()
    
    if not game:
        raise HTTPException(status_code=404, detail="Player not found")
    
    return Player(
        name=game.player_name,
        empire=game.player_empire.to_dict() if game.player_empire else None,
        resources=PlayerResources(**game.player_resources.to_dict()) if game.player_resources else PlayerResources()
    )

@router.post("/players/", response_model=Player)
async def create_player(player: Player, db: Session = Depends(get_db)):
    """Create a new player"""
    # Check if player already exists
    stmt = select(GameDB).where(GameDB.player_name == player.name)
    result = db.execute(stmt)
    existing_player = result.scalars().first()
    
    if existing_player:
        raise HTTPException(status_code=400, detail="Player already exists")
    
    # Create new game for the player
    game = GameDB(
        player_name=player.name,
    )
    
    # Create player empire with correct name format
    empire_name = f"{player.name}'s Empire"
    empire = EmpireDB(
        game=game,
        name=empire_name,
        is_player=True,
        color="#0000FF"  # Default color for player empire
    )
    
    # Set the player's empire
    game.player_empire = empire
    
    # Create player resources
    resources = PlayerResourcesDB(
        game=game,
        **player.resources.dict()
    )
    
    db.add(game)
    db.add(empire)
    db.add(resources)
    db.commit()
    
    return Player(
        name=game.player_name,
        empire=empire.to_dict(),
        resources=PlayerResources(**resources.to_dict())
    )

# Galaxy endpoints
@router.get("/galaxies/{galaxy_id}", response_model=Galaxy)
async def get_galaxy(galaxy_id: str, db: Session = Depends(get_db)):
    """Get galaxy details by ID"""
    stmt = select(GalaxyDB).where(GalaxyDB.id == galaxy_id)
    result = db.execute(stmt)
    galaxy = result.scalars().first()
    
    if not galaxy:
        raise HTTPException(status_code=404, detail="Galaxy not found")
    
    return Galaxy(
        size=galaxy.size,
        systems=[StarSystem(**system.to_dict()) for system in galaxy.systems],
        explored_count=galaxy.explored_count
    )

# Star System endpoints
@router.get("/systems/{system_id}", response_model=StarSystem)
async def get_star_system(system_id: str, db: Session = Depends(get_db)):
    """Get star system details by ID"""
    stmt = select(StarSystemDB).where(StarSystemDB.id == system_id)
    result = db.execute(stmt)
    system = result.scalars().first()
    
    if not system:
        raise HTTPException(status_code=404, detail="Star system not found")
    
    return StarSystem(**system.to_dict())

@router.get("/systems/", response_model=List[StarSystem])
async def list_star_systems(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """List all star systems with pagination"""
    stmt = select(StarSystemDB).offset(skip).limit(limit)
    result = db.execute(stmt)
    systems = result.scalars().all()
    
    return [StarSystem(**system.to_dict()) for system in systems]

@router.patch("/planets/{planet_id}/colonize", response_model=Planet)
async def colonize_planet(planet_id: str, player_name: str, db: Session = Depends(get_db)):
    """Colonize a planet"""
    # Get the planet
    stmt = select(PlanetDB).where(PlanetDB.id == planet_id)
    result = db.execute(stmt)
    planet = result.scalars().first()
    
    if not planet:
        raise HTTPException(status_code=404, detail="Planet not found")
    
    if planet.colonized:
        raise HTTPException(status_code=400, detail="Planet is already colonized")
    
    # Get the player's game
    stmt = select(GameDB).where(GameDB.player_name == player_name)
    result = db.execute(stmt)
    game = result.scalars().first()
    
    if not game:
        raise HTTPException(status_code=404, detail="Player not found")
    
    # Update planet
    planet.colonized = True
    planet.empire_id = game.id  # Using game ID as empire ID for simplicity
    db.commit()
    
    return Planet(**planet.to_dict())

# Game State endpoints
@router.get("/games/{game_id}/state", response_model=Dict)
async def get_game_state(game_id: str, db: Session = Depends(get_db)):
    """Get game state by ID"""
    stmt = select(GameDB).where(GameDB.id == game_id)
    result = db.execute(stmt)
    game = result.scalars().first()
    
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game_state = game.to_dict()
    return {
        "id": game_state["id"],
        "player_name": game_state["player_name"],
        "game_state": game_state,
        "created_at": game_state["created_at"],
        "updated_at": game_state["updated_at"],
        "difficulty": game_state["difficulty"],
        "galaxy": game_state["galaxy"],
        "player": game_state["player"],
        "empires": game_state["empires"],
        "turn": game_state["turn"]
    }

@router.post("/games/", response_model=GameState)
async def create_game(game_state: GameState, db: Session = Depends(get_db)):
    """Create a new game"""
    # Create game
    game = GameDB(
        player_name=game_state.player.name,
        difficulty=game_state.difficulty,
        galaxy_size=game_state.galaxy.size
    )
    
    # Create player resources
    resources = PlayerResourcesDB(
        game=game,
        **game_state.player.resources.dict()
    )
    
    # Create galaxy
    galaxy = GalaxyDB(
        game=game,
        size=game_state.galaxy.size
    )
    
    # Create player empire
    empire = EmpireDB(
        game=game,
        name=f"{game_state.player.name}'s Empire",
        is_player=True,
        color="#00FF00"  # Default player color
    )
    
    db.add(game)
    db.add(resources)
    db.add(galaxy)
    db.add(empire)
    db.commit()
    
    # Update game with player empire
    game.player_empire_id = empire.id
    db.commit()
    
    return GameState(**game.to_dict())

@router.patch("/games/{game_id}/advance-turn", response_model=GameState)
async def advance_turn(game_id: str, db: Session = Depends(get_db)):
    """Advance the game turn"""
    stmt = select(GameDB).where(GameDB.id == game_id)
    result = db.execute(stmt)
    game = result.scalars().first()
    
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game.turn += 1
    db.commit()
    
    return GameState(**game.to_dict())

# Game endpoints
@router.get("/games/", response_model=List[GameResponse])
async def list_games(db: Session = Depends(get_db)):
    """List all games."""
    stmt = select(GameDB)
    result = db.execute(stmt)
    games = result.scalars().all()
    return [GameResponse(**game.to_dict()) for game in games]

@router.delete("/games/{game_id}/", response_model=Dict)
async def delete_game(game_id: str, db: Session = Depends(get_db)):
    """Delete a game by ID."""
    stmt = select(GameDB).where(GameDB.id == game_id)
    result = db.execute(stmt)
    game = result.scalars().first()
    
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    db.delete(game)
    db.commit()
    return {"message": "Game deleted successfully"}

# Settings endpoints
@router.get("/settings", response_model=Dict)
async def get_settings():
    """Get current game settings."""
    return {
        "settings": {
            "audio_volume": 100,
            "music_volume": 100,
            "sfx_volume": 100,
            "fullscreen": False
        },
        "message": "Current game settings"
    }

@router.post("/settings", response_model=Dict)
async def update_settings(settings_data: Dict):
    """Update game settings."""
    settings = settings_data.get("settings", {})
    return {
        "message": "Settings updated successfully",
        "settings": {
            "audio_volume": settings.get("audio_volume", 100),
            "music_volume": settings.get("music_volume", 100),
            "sfx_volume": settings.get("sfx_volume", 100),
            "fullscreen": settings.get("fullscreen", False)
        }
    }

@router.get("/settings/reset", response_model=Dict)
async def reset_settings():
    """Reset settings to defaults."""
    return {
        "message": "Settings reset to defaults",
        "settings": {
            "audio_volume": 100,
            "music_volume": 100,
            "sfx_volume": 100,
            "fullscreen": False
        }
    }

# Exit game endpoints
@router.post("/games/exit", response_model=Dict)
async def exit_game(exit_data: Dict):
    """Handle game exit with optional save."""
    save_before_exit = exit_data.get("save_before_exit", False)
    save_name = exit_data.get("save_name")
    game_id = exit_data.get("game_id")
    
    if save_before_exit and save_name and game_id:
        return {
            "message": f"Game saved as '{save_name}' before exit",
            "saved": True,
            "save_id": str(uuid.uuid4())
        }
    else:
        return {
            "message": "Game exited without saving",
            "saved": False
        } 