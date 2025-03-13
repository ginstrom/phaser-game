from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, JSON, DateTime, func, Table
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from app.database.config import Base
from app.models.empire import EmpireDB, empire_systems

def generate_uuid():
    """Generate a UUID string for use as a primary key."""
    return str(uuid.uuid4())

class Game(Base):
    """SQLAlchemy model for a game."""
    __tablename__ = "games"

    id = Column(String, primary_key=True, default=generate_uuid)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Player info
    player_name = Column(String, nullable=False)
    player_empire_id = Column(String, ForeignKey("empires.id", use_alter=True, name='fk_game_player_empire_id'), nullable=True)
    
    # Game settings
    difficulty = Column(String, nullable=False, default="normal")
    galaxy_size = Column(String, nullable=False, default="medium")
    
    # Game state
    turn = Column(Integer, default=1)
    
    # Related entities
    galaxy = relationship("Galaxy", uselist=False, back_populates="game", cascade="all, delete-orphan")
    player_resources = relationship("PlayerResources", uselist=False, back_populates="game", cascade="all, delete-orphan")
    empires = relationship("EmpireDB", back_populates="game", foreign_keys="[EmpireDB.game_id]", cascade="all, delete-orphan")
    player_empire = relationship("EmpireDB", foreign_keys=[player_empire_id], post_update=True)
    
    def to_dict(self):
        """Convert the game to a dictionary for API responses."""
        # Get empire data with a default if None
        empire_data = self.player_empire.to_dict() if self.player_empire else {
            "name": f"{self.player_name}'s Empire",
            "is_player": True,
            "color": "#0000FF",
            "credits": 1000,
            "research_points": 0
        }
        
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "player_name": self.player_name,
            "player_empire_id": self.player_empire_id,
            "difficulty": self.difficulty,
            "galaxy_size": self.galaxy_size,
            "turn": self.turn,
            "player": {
                "name": self.player_name,
                "empire": empire_data,
                "resources": self.player_resources.to_dict() if self.player_resources else {
                    "organic": 0,
                    "mineral": 500,
                    "energy": 200,
                    "exotics": 0,
                    "credits": 1000,
                    "research": 0
                }
            },
            "galaxy": self.galaxy.to_dict() if self.galaxy else {
                "size": self.galaxy_size,
                "systems": [],
                "explored_count": 0
            },
            "empires": [empire.to_dict() for empire in self.empires] if self.empires else []
        }


class Galaxy(Base):
    """SQLAlchemy model for a galaxy."""
    __tablename__ = "galaxies"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    game_id = Column(String, ForeignKey("games.id", ondelete="CASCADE"), nullable=False)
    size = Column(String, nullable=False)
    explored_count = Column(Integer, default=0)
    
    # Related entities
    game = relationship("Game", back_populates="galaxy")
    systems = relationship("StarSystem", back_populates="galaxy", cascade="all, delete-orphan")
    
    @property
    def total_systems(self):
        """Get the total number of star systems in the galaxy."""
        return len(self.systems)
    
    def to_dict(self):
        """Convert the galaxy to a dictionary for the API response."""
        return {
            "id": self.id,
            "size": self.size,
            "explored_count": self.explored_count,
            "total_systems": self.total_systems,
            "systems": [system.to_dict() for system in self.systems] if self.systems else []
        }


class StarSystem(Base):
    """SQLAlchemy model for a star system."""
    __tablename__ = "star_systems"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    galaxy_id = Column(String, ForeignKey("galaxies.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    position_x = Column(Float, nullable=False)
    position_y = Column(Float, nullable=False)
    explored = Column(Boolean, default=False)
    discovery_level = Column(Integer, default=0)  # 0: visible light, 1-5: scanning levels, 6: visited
    
    # Related entities
    galaxy = relationship("Galaxy", back_populates="systems")
    planets = relationship("Planet", back_populates="system", cascade="all, delete-orphan")
    controlling_empire = relationship("EmpireDB", secondary="empire_systems", back_populates="controlled_systems")
    
    def to_dict(self):
        """Convert the star system to a dictionary for the API response."""
        return {
            "id": self.id,
            "name": self.name,
            "position_x": self.position_x,
            "position_y": self.position_y,
            "position": {"x": self.position_x, "y": self.position_y},
            "explored": self.explored,
            "discovery_level": self.discovery_level,
            "planets": [planet.to_dict() for planet in self.planets] if self.planets else []
        }


class Planet(Base):
    """SQLAlchemy model for a planet."""
    __tablename__ = "planets"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    system_id = Column(String, ForeignKey("star_systems.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    colonized = Column(Boolean, default=False)
    empire_id = Column(String, ForeignKey("empires.id", ondelete="SET NULL"), nullable=True)
    
    # Related entities
    system = relationship("StarSystem", back_populates="planets")
    resources = relationship("PlanetResources", uselist=False, back_populates="planet", cascade="all, delete-orphan")
    empire = relationship("EmpireDB", back_populates="controlled_planets")
    
    def to_dict(self):
        """Convert the planet to a dictionary for the API response."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "size": self.size,
            "colonized": self.colonized,
            "empire_id": self.empire_id,
            "owner": self.empire_id,
            "resources": self.resources.to_dict() if self.resources else {}
        }


class PlanetResources(Base):
    """SQLAlchemy model for planet resources."""
    __tablename__ = "planet_resources"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    planet_id = Column(String, ForeignKey("planets.id", ondelete="CASCADE"), nullable=False)
    organic = Column(Integer, default=0)
    mineral = Column(Integer, default=0)
    energy = Column(Integer, default=0)
    exotics = Column(Integer, default=0)
    
    # Related entities
    planet = relationship("Planet", back_populates="resources")
    
    def to_dict(self):
        """Convert the planet resources to a dictionary for the API response."""
        return {
            "organic": self.organic,
            "mineral": self.mineral,
            "energy": self.energy,
            "exotics": self.exotics
        }


class PlayerResources(Base):
    """SQLAlchemy model for player resources."""
    __tablename__ = "player_resources"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    game_id = Column(String, ForeignKey("games.id", ondelete="CASCADE"), nullable=False)
    organic = Column(Integer, default=0)
    mineral = Column(Integer, default=500)
    energy = Column(Integer, default=200)
    exotics = Column(Integer, default=0)
    credits = Column(Integer, default=1000)
    research = Column(Integer, default=0)
    
    # Related entities
    game = relationship("Game", back_populates="player_resources")
    
    def to_dict(self):
        """Convert the player resources to a dictionary for the API response."""
        return {
            "organic": self.organic,
            "mineral": self.mineral,
            "energy": self.energy,
            "exotics": self.exotics,
            "credits": self.credits,
            "research": self.research
        }

class GameStateDB(Base):
    __tablename__ = "game_states"

    id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    player_name = Column(String, nullable=False)
    empire_name = Column(String, nullable=False)
    turn = Column(Integer, default=1)
    difficulty = Column(String, nullable=False)
    game_data = Column(JSON, nullable=False)  # Stores the complete game state as JSON

    def to_dict(self):
        return {
            "game_id": self.id,
            "player_name": self.player_name,
            "empire_name": self.empire_name,
            "turn": self.turn,
            "save_date": self.updated_at.isoformat(),
            "game_state": self.game_data
        }