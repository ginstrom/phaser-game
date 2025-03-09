from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, JSON, DateTime, func
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from app.database.config import Base

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
    empire_name = Column(String, default="Human Empire")
    
    # Game settings
    difficulty = Column(String, nullable=False, default="normal")
    galaxy_size = Column(String, nullable=False, default="medium")
    
    # Game state
    turn = Column(Integer, default=1)
    
    # Related entities
    galaxy = relationship("Galaxy", uselist=False, back_populates="game", cascade="all, delete-orphan")
    player_resources = relationship("PlayerResources", uselist=False, back_populates="game", cascade="all, delete-orphan")
    
    def to_dict(self):
        """Convert the game to a dictionary for the API response."""
        player = {
            "name": self.player_name,
            "empire": self.empire_name,
            "resources": self.player_resources.to_dict() if self.player_resources else {}
        }
        
        # Ensure galaxy is loaded
        galaxy_data = {
            "size": self.galaxy_size,
            "systems": 0,
            "explored": 0
        }
        
        if self.galaxy:
            galaxy_data["systems"] = self.galaxy.total_systems
            galaxy_data["explored"] = self.galaxy.explored_count
            if hasattr(self.galaxy, 'to_dict'):
                galaxy_data.update(self.galaxy.to_dict())
        
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "player": player,
            "galaxy": galaxy_data,
            "turn": self.turn,
            "difficulty": self.difficulty
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
    
    def to_dict(self):
        """Convert the star system to a dictionary for the API response."""
        return {
            "id": self.id,
            "name": self.name,
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
    owner = Column(String, nullable=True)
    
    # Related entities
    system = relationship("StarSystem", back_populates="planets")
    resources = relationship("PlanetResources", uselist=False, back_populates="planet", cascade="all, delete-orphan")
    
    def to_dict(self):
        """Convert the planet to a dictionary for the API response."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "size": self.size,
            "colonized": self.colonized,
            "owner": self.owner,
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