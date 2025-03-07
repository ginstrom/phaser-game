import random
import string
from typing import Dict, List, Any, Optional
import math

from backend.models.game import (
    GameState,
    Player,
    Galaxy,
    StarSystem,
    Planet,
    PlanetResources
)

# In-memory storage for games (would be replaced with a database in production)
games: Dict[str, GameState] = {}

# Planet type probabilities based on distance from star
PLANET_TYPES = [
    "rocky", "terrestrial", "oceanic", "desert", "jungle", 
    "arctic", "gas giant", "ice giant", "volcanic"
]

# Star system name components for random generation
STAR_NAME_PREFIXES = [
    "Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta",
    "Iota", "Kappa", "Lambda", "Mu", "Nu", "Xi", "Omicron", "Pi", "Rho",
    "Sigma", "Tau", "Upsilon", "Phi", "Chi", "Psi", "Omega"
]

STAR_NAME_SUFFIXES = [
    "Centauri", "Cygni", "Draconis", "Eridani", "Hydri", "Leonis", "Orionis",
    "Persei", "Tauri", "Ursae", "Virginis", "Serpentis", "Aquilae", "Lyrae"
]

# Planet name components for random generation
PLANET_NAME_PREFIXES = [
    "New", "Old", "Great", "Lesser", "Upper", "Lower", "Inner", "Outer",
    "Northern", "Southern", "Eastern", "Western", "Central", "Prime"
]

PLANET_NAME_SUFFIXES = [
    "Terra", "Earth", "Mars", "Venus", "Jupiter", "Saturn", "Uranus", "Neptune",
    "Pluto", "Mercury", "Ceres", "Eris", "Haumea", "Makemake", "Sedna"
]


def generate_star_system_name() -> str:
    """Generate a random star system name."""
    if random.random() < 0.7:  # 70% chance of a prefix-suffix name
        prefix = random.choice(STAR_NAME_PREFIXES)
        suffix = random.choice(STAR_NAME_SUFFIXES)
        return f"{prefix} {suffix}"
    else:  # 30% chance of a name with a number
        prefix = random.choice(STAR_NAME_PREFIXES)
        number = random.randint(1, 999)
        return f"{prefix}-{number}"


def generate_planet_name() -> str:
    """Generate a random planet name."""
    if random.random() < 0.6:  # 60% chance of a prefix-suffix name
        prefix = random.choice(PLANET_NAME_PREFIXES)
        suffix = random.choice(PLANET_NAME_SUFFIXES)
        return f"{prefix} {suffix}"
    else:  # 40% chance of a single name with a number
        suffix = random.choice(PLANET_NAME_SUFFIXES)
        number = random.randint(1, 9)
        return f"{suffix} {number}"


def generate_planet(position_in_system: int) -> Planet:
    """Generate a random planet based on its position in the star system."""
    # Planet type probabilities based on position
    if position_in_system <= 2:  # Inner planets
        planet_types = ["rocky", "terrestrial", "volcanic"]
        weights = [0.5, 0.3, 0.2]
    elif position_in_system <= 4:  # Middle planets
        planet_types = ["terrestrial", "oceanic", "desert", "jungle", "arctic"]
        weights = [0.3, 0.2, 0.2, 0.15, 0.15]
    else:  # Outer planets
        planet_types = ["gas giant", "ice giant", "arctic"]
        weights = [0.5, 0.4, 0.1]
    
    planet_type = random.choices(planet_types, weights=weights, k=1)[0]
    
    # Planet size based on type
    if planet_type in ["gas giant", "ice giant"]:
        size = random.randint(7, 10)
    elif planet_type in ["terrestrial", "oceanic", "jungle"]:
        size = random.randint(4, 7)
    else:
        size = random.randint(1, 5)
    
    return Planet(
        name=generate_planet_name(),
        type=planet_type,
        size=size
    )


def generate_star_system(position: Dict[str, float]) -> StarSystem:
    """Generate a random star system at the given position."""
    system = StarSystem(
        name=generate_star_system_name(),
        position=position,
        planets=[]
    )
    
    # Generate 1-8 planets for the system
    num_planets = random.randint(1, 8)
    for i in range(num_planets):
        system.planets.append(generate_planet(i + 1))
    
    return system


def generate_galaxy(size: str) -> Galaxy:
    """Generate a galaxy with random star systems based on the specified size."""
    # Determine number of star systems based on galaxy size
    if size == "small":
        num_systems = random.randint(10, 20)
    elif size == "medium":
        num_systems = random.randint(20, 40)
    else:  # large
        num_systems = random.randint(40, 60)
    
    galaxy = Galaxy(size=size, systems=[])
    
    # Generate star systems with random positions
    for _ in range(num_systems):
        # Generate random position within a circular galaxy
        radius = random.random()  # 0 to 1
        angle = random.random() * 2 * math.pi  # 0 to 2π
        
        # Convert polar coordinates to Cartesian
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        
        galaxy.systems.append(generate_star_system({"x": x, "y": y}))
    
    # Mark the first system as explored
    if galaxy.systems:
        galaxy.systems[0].explored = True
        galaxy.explored_count = 1
    
    return galaxy


def create_new_game(player_name: str, difficulty: str = "normal", galaxy_size: str = "medium") -> GameState:
    """Create a new game with the specified parameters."""
    # Create player
    player = Player(name=player_name)
    
    # Generate galaxy
    galaxy = generate_galaxy(galaxy_size)
    
    # Create game state
    game = GameState(
        player=player,
        galaxy=galaxy,
        difficulty=difficulty
    )
    
    # Store game in memory
    games[game.id] = game
    
    return game


def get_game(game_id: str) -> Optional[GameState]:
    """Get a game by ID."""
    return games.get(game_id)


def get_all_games() -> List[GameState]:
    """Get all games."""
    return list(games.values())


def delete_game(game_id: str) -> bool:
    """Delete a game by ID."""
    if game_id in games:
        del games[game_id]
        return True
    return False
