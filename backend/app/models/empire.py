from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Float, JSON, Table
from sqlalchemy.orm import relationship
from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict
from datetime import datetime

from app.database.models import Base
from app.utils.id_gen import generate_uuid

# Association table for empire-system relationships
empire_systems = Table(
    'empire_systems',
    Base.metadata,
    Column('empire_id', String, ForeignKey('empires.id')),
    Column('system_id', String, ForeignKey('star_systems.id'))
)

class Empire(Base):
    """SQLAlchemy model for an empire."""
    __tablename__ = "empires"

    id = Column(String, primary_key=True, default=generate_uuid)
    game_id = Column(String, ForeignKey("games.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    is_player = Column(Boolean, default=False)
    color = Column(String, nullable=False)  # Hex color code
    
    # Resources
    credits = Column(Integer, default=1000)
    research_points = Column(Integer, default=0)
    
    # Research levels (stored as JSON)
    research_levels = Column(JSON, default=lambda: {
        "weapons": 0,
        "shields": 0,
        "propulsion": 0,
        "economics": 0
    })
    
    # Relationships
    game = relationship("Game", back_populates="empires")
    controlled_systems = relationship("StarSystem", secondary=empire_systems, back_populates="controlling_empire")
    controlled_planets = relationship("Planet", back_populates="empire")

    def to_dict(self):
        """Convert the empire to a dictionary for API responses."""
        return {
            "id": self.id,
            "name": self.name,
            "is_player": self.is_player,
            "color": self.color,
            "credits": self.credits,
            "research_points": self.research_points,
            "research_levels": self.research_levels,
            "controlled_systems_count": len(self.controlled_systems),
            "controlled_planets_count": len(self.controlled_planets)
        }

# Pydantic models for API
class EmpireBase(BaseModel):
    name: str
    color: str
    is_player: bool = False

class EmpireCreate(EmpireBase):
    pass

class EmpireUpdate(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None
    credits: Optional[int] = None
    research_points: Optional[int] = None
    research_levels: Optional[Dict[str, int]] = None

class EmpireResponse(EmpireBase):
    id: str
    credits: int
    research_points: int
    research_levels: Dict[str, int]
    controlled_systems_count: int
    controlled_planets_count: int

    model_config = ConfigDict(from_attributes=True) 