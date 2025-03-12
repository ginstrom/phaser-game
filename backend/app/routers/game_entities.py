"""Game entities router handling core game state and actions.
* Manages CRUD operations for players, galaxies, star systems, and planets
* Handles game state operations like colonization and turn advancement
* Provides endpoints for retrieving game state and entity information
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.game import (
    GameState,
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
    PlayerResources as PlayerResourcesDB
)

router = APIRouter(prefix="/api/v1")

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
        empire=game.empire_name,
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
        empire_name=player.empire
    )
    
    # Create player resources
    resources = PlayerResourcesDB(
        game=game,
        **player.resources.dict()
    )
    
    db.add(game)
    db.add(resources)
    db.commit()
    
    return player

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
@router.get("/games/{game_id}", response_model=GameState)
async def get_game_state(game_id: str, db: Session = Depends(get_db)):
    """Get game state by ID"""
    stmt = select(GameDB).where(GameDB.id == game_id)
    result = db.execute(stmt)
    game = result.scalars().first()
    
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    return GameState(**game.to_dict())

@router.post("/games/", response_model=GameState)
async def create_game(game_state: GameState, db: Session = Depends(get_db)):
    """Create a new game"""
    # Create game
    game = GameDB(
        player_name=game_state.player.name,
        empire_name=game_state.player.empire,
        difficulty=game_state.difficulty.value,
        galaxy_size=game_state.galaxy.size.value
    )
    
    # Create player resources
    resources = PlayerResourcesDB(
        game=game,
        **game_state.player.resources.dict()
    )
    
    # Create galaxy
    galaxy = GalaxyDB(
        game=game,
        size=game_state.galaxy.size.value
    )
    
    db.add(game)
    db.add(resources)
    db.add(galaxy)
    db.commit()
    
    return GameState(**game.to_dict())

@router.patch("/games/{game_id}/turn", response_model=GameState)
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