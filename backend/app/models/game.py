from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid
import random
from enum import Enum

from app.config import PlanetType, GalaxySize, Difficulty
from .empire import EmpireBase


class PlanetResources(BaseModel):
    """Model representing resources available on a planet."""
    organic: int = Field(default_factory=lambda: random.randint(0, 100))
    mineral: int = Field(default_factory=lambda: random.randint(0, 100))
    energy: int = Field(default_factory=lambda: random.randint(0, 100))
    exotics: int = Field(default_factory=lambda: random.randint(0, 100))


class PlayerResources(BaseModel):
    """Model representing player resources in the game."""
    organic: int = 0
    mineral: int = 500
    energy: int = 200
    exotics: int = 0
    credits: int = 1000
    research: int = 0


class Player(BaseModel):
    """Model representing a player in the game."""
    name: str
    empire: Optional[str | Dict[str, Any]] = "Human Empire"
    resources: PlayerResources = Field(default_factory=PlayerResources)


class Planet(BaseModel):
    """Model representing a planet in the game."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    type: PlanetType  # Planet type enum
    size: int  # 1-10 scale
    resources: PlanetResources = Field(default_factory=PlanetResources)
    colonized: bool = False
    owner: Optional[str] = None  # player name if colonized


class StarSystem(BaseModel):
    """Model representing a star system in the game."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    position: Dict[str, float]  # x, y coordinates in the galaxy
    planets: List[Planet] = []
    explored: bool = False


class Galaxy(BaseModel):
    """Model representing the galaxy in the game."""
    size: GalaxySize  # Galaxy size enum
    systems: List[StarSystem] = []
    explored_count: int = 0

    @property
    def total_systems(self) -> int:
        return len(self.systems)


class GameState(BaseModel):
    """Model representing the complete state of a game."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    player: Player
    galaxy: Galaxy
    turn: int = 1
    difficulty: Difficulty  # Difficulty enum
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the game state to a dictionary for API responses."""
        return {
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
                "size": self.galaxy.size.value,
                "systems": self.galaxy.total_systems,
                "explored": self.galaxy.explored_count
            },
            "turn": self.turn
        }
