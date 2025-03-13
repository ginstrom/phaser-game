from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import uuid
import random
from enum import Enum
from sqlalchemy import Column, String, ForeignKey

from app.config import PlanetType, GalaxySize, Difficulty
from app.models.empire import EmpireDB, EmpireResponse


class PlanetResources(BaseModel):
    """Model representing resources available on a planet."""
    organic: int = Field(default_factory=lambda: random.randint(0, 100))
    mineral: int = Field(default_factory=lambda: random.randint(0, 100))
    energy: int = Field(default_factory=lambda: random.randint(0, 100))
    exotics: int = Field(default_factory=lambda: random.randint(0, 100))

    model_config = ConfigDict(from_attributes=True)


class PlayerResources(BaseModel):
    """Model representing player's resources."""
    organic: int = 0
    mineral: int = 0
    energy: int = 0
    exotics: int = 0
    credits: int = 1000
    research: int = 0

    model_config = ConfigDict(from_attributes=True)


class Player(BaseModel):
    """Model representing a player in the game."""
    name: str
    empire: Union[str, Dict[str, Any]] = "Human Empire"
    resources: PlayerResources = Field(default_factory=PlayerResources)

    model_config = ConfigDict(from_attributes=True)


class Planet(BaseModel):
    """Model representing a planet in the game."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    type: str  # "terrestrial", "gas_giant", etc.
    size: int  # 1-10
    resources: Optional[PlanetResources] = None
    owner: Optional[str] = None  # ID of empire that owns this planet
    colonized: bool = False


class StarSystem(BaseModel):
    """Model representing a star system in the game."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    position_x: float  # 0.0 to 1.0
    position_y: float  # 0.0 to 1.0
    planets: List[Planet] = []
    explored: bool = False
    discovery_level: int = 0  # 0=undiscovered, 1=detected, 2=scanned, 3=surveyed, 4=explored, 5=visited


class Galaxy(BaseModel):
    """Model representing the game galaxy."""
    size: str
    total_systems: int = 0
    explored_count: int = 0

    model_config = ConfigDict(from_attributes=True)


class GameState(BaseModel):
    """Model representing the complete state of a game."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    player_name: str
    player: Player
    galaxy: Galaxy
    turn: int = 1
    difficulty: str  # "easy", "normal", "hard"
    empires: List[EmpireResponse] = []
    
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        from_attributes=True
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the game state to a dictionary for API responses."""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "player_name": self.player_name,
            "player": {
                "name": self.player.name,
                "empire": self.player.empire,
                "resources": {
                    "organic": self.player.resources.organic,
                    "mineral": self.player.resources.mineral,
                    "energy": self.player.resources.energy,
                    "exotics": self.player.resources.exotics,
                    "credits": self.player.resources.credits,
                    "research": self.player.resources.research
                }
            },
            "galaxy": {
                "size": self.galaxy.size,
                "systems": self.galaxy.total_systems,
                "explored": self.galaxy.explored_count
            },
            "turn": self.turn,
            "difficulty": self.difficulty,
            "empires": [empire.model_dump() for empire in self.empires]
        }


class GameCreate(BaseModel):
    """Model for creating a new game."""
    player_name: str
    difficulty: str = "normal"
    galaxy_size: str = "medium"
    player_resources: Optional[Dict[str, int]] = None


class GameResponse(BaseModel):
    """Model for game response data."""
    id: str
    created_at: datetime
    updated_at: datetime
    player_name: str
    player_empire_id: Optional[str] = None
    difficulty: str
    galaxy_size: str
    turn: int
    empires: List[EmpireResponse]
    player: Dict[str, Any]
    galaxy: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)


class Game:
    def __init__(self, id: str, player_name: str, difficulty: str, galaxy_size: str, created_at: datetime = None):
        self.id = id
        self.player_name = player_name
        self.difficulty = difficulty
        self.galaxy_size = galaxy_size
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert the game to a dictionary representation."""
        return {
            "id": self.id,
            "player_name": self.player_name,
            "difficulty": self.difficulty,
            "galaxy_size": self.galaxy_size,
            "created_at": self.created_at.isoformat(),
            "galaxy": {
                "size": self.galaxy_size,
                "systems": [system.to_dict() for system in self.galaxy.systems] if hasattr(self, 'galaxy') else []
            },
            "player": {
                "name": self.player_name,
                "empire": self.player_empire.to_dict() if hasattr(self, 'player_empire') else None,
                "resources": self.player_resources.to_dict() if hasattr(self, 'player_resources') else None
            }
        }

    def __getitem__(self, key: str) -> Any:
        """Make the game model subscriptable."""
        return self.to_dict()[key]
