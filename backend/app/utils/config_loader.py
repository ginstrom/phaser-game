import json
from pathlib import Path
from typing import Dict, List, Any, TypeVar, cast, Optional
from pydantic import BaseModel, Field, ConfigDict
import yaml
import os

T = TypeVar('T')

class GameEnums(BaseModel):
    PlanetType: List[str] = Field(..., description="Available planet types")
    GalaxySize: List[str] = Field(..., description="Available galaxy sizes")
    Difficulty: List[str] = Field(..., description="Available difficulty levels")
    ResearchArea: List[str] = Field(..., description="Available research areas")
    PerkAttribute: List[str] = Field(..., description="Available perk attributes")

class GalaxyConfig(BaseModel):
    width: int
    height: int
    min_systems: int
    max_systems: int

class GameSettings(BaseModel):
    """Model for game settings configuration."""
    min_computer_empires: int
    max_computer_empires: int
    default_computer_empires: int
    galaxy_sizes: Dict[str, int]
    difficulties: List[str]

    model_config = ConfigDict(from_attributes=True)

class EmpirePerks(BaseModel):
    """Model for empire perks configuration."""
    research_efficiency: float
    combat_efficiency: float
    economic_efficiency: float
    diplomatic_influence: float

    model_config = ConfigDict(from_attributes=True)

class StartingResources(BaseModel):
    """Model for starting resources configuration."""
    credits: int
    research_points: int

    model_config = ConfigDict(from_attributes=True)

class ResearchLevels(BaseModel):
    weapons: int
    shields: int
    propulsion: int
    economics: int

class GameDefaults(BaseModel):
    perks: EmpirePerks
    starting_resources: Dict[str, StartingResources]
    research_levels: ResearchLevels

class EmpireArchetype(BaseModel):
    """Model for empire archetype configuration."""
    name: str
    perks: EmpirePerks
    color_range: List[str]

    model_config = ConfigDict(from_attributes=True)

class PerkPointAllocation(BaseModel):
    total_points: int
    min_per_attribute: int
    max_per_attribute: int

class GameConfig(BaseModel):
    defaults: GameDefaults
    empire_archetypes: List[EmpireArchetype]
    perk_point_allocation: PerkPointAllocation
    game_settings: GameSettings

class Config:
    """Configuration loader and manager."""
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'game_config.yaml')
        
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
    
    def get_config_section(self, *sections: str) -> Any:
        """Get a configuration section by path."""
        current = self.config
        for section in sections:
            if section not in current:
                raise KeyError(f"Configuration section {section} not found")
            current = current[section]
        
        # Convert to appropriate model if needed
        if sections[0] == "defaults":
            if sections[1] == "starting_resources":
                return {k: StartingResources(**v) for k, v in current.items()}
            elif sections[1] == "perks":
                return EmpirePerks(**current)
        elif sections[0] == "empire_archetypes":
            if len(sections) == 1:
                return [EmpireArchetype(**archetype) for archetype in current]
        elif sections[0] == "game_settings":
            return GameSettings(**current)
        
        return current

# Global config instance
config = Config()

# Example usage:
# from app.utils.config_loader import config
# 
# # Get enums
# planet_types = config.get_enum("PlanetType")
# 
# # Get configuration
# default_perks = config.get_config_section("defaults", "perks")
# starting_resources = config.get_config_section("defaults", "starting_resources")
# archetype = config.get_config_section("empire_archetypes")[0] 