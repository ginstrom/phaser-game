import random
import math
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database.models import (
    Game, Galaxy, StarSystem, Planet,
    PlanetResources, PlayerResources
)
from app.services.empire_service import initialize_game_empires

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

class GameRepository:
    """Repository for game operations with synchronous SQLAlchemy."""
    def __init__(self, session: Session):
        self.session = session

    def create_game(self, game_data):
        """Create a new game with the specified parameters."""
        # Extract basic game info
        if isinstance(game_data, dict):
            player_name = game_data.get("player_name")
            difficulty = game_data.get("difficulty", "normal")
            galaxy_size = game_data.get("galaxy_size", "medium")
            player_resources_data = game_data.get("player_resources", {})
        else:
            player_name = game_data.player_name
            difficulty = getattr(game_data, 'difficulty', 'normal')
            galaxy_size = getattr(game_data, 'galaxy_size', 'medium')
            player_resources_data = getattr(game_data, 'player_resources', {}) or {}
        
        # Create the game
        game = Game(
            player_name=player_name,
            difficulty=difficulty,
            galaxy_size=galaxy_size
        )
        
        # Create player resources
        player_resources = PlayerResources(
            game=game,
            organic=player_resources_data.get("organic", 0),
            mineral=player_resources_data.get("mineral", 500),
            energy=player_resources_data.get("energy", 200),
            exotics=player_resources_data.get("exotics", 0),
            credits=player_resources_data.get("credits", 1000),
            research=player_resources_data.get("research", 0)
        )
        
        # Create galaxy
        galaxy = self._generate_galaxy(game, galaxy_size)
        
        # Add to session
        self.session.add(game)
        self.session.add(player_resources)
        self.session.add(galaxy)
        self.session.commit()
        
        # Initialize empires
        initialize_game_empires(
            self.session,
            game.id,
            player_name,
            difficulty=difficulty
        )
        
        return game

    def get_game_by_id(self, game_id: str):
        """Get a game by ID."""
        stmt = select(Game).where(Game.id == game_id)
        result = self.session.execute(stmt)
        game = result.scalars().first()
        
        # Ensure relationships are loaded
        if game:
            # Load player resources
            if not game.player_resources:
                stmt = select(PlayerResources).where(PlayerResources.game_id == game_id)
                result = self.session.execute(stmt)
                player_resources = result.scalars().first()
                if player_resources:
                    game.player_resources = player_resources
            
            # Load galaxy
            if not game.galaxy:
                stmt = select(Galaxy).where(Galaxy.game_id == game_id)
                result = self.session.execute(stmt)
                galaxy = result.scalars().first()
                if galaxy:
                    game.galaxy = galaxy
        
        return game

    def list_games(self):
        """List all saved games."""
        stmt = select(Game)
        result = self.session.execute(stmt)
        games = result.scalars().all()
        
        # Ensure relationships are loaded for each game
        for game in games:
            # Load player resources
            if not game.player_resources:
                stmt = select(PlayerResources).where(PlayerResources.game_id == game.id)
                result = self.session.execute(stmt)
                player_resources = result.scalars().first()
                if player_resources:
                    game.player_resources = player_resources
            
            # Load galaxy
            if not game.galaxy:
                stmt = select(Galaxy).where(Galaxy.game_id == game.id)
                result = self.session.execute(stmt)
                galaxy = result.scalars().first()
                if galaxy:
                    game.galaxy = galaxy
        
        return games

    def delete_game(self, game_id: str):
        """Delete a game by ID."""
        game = self.get_game_by_id(game_id)
        if game:
            self.session.delete(game)
            self.session.commit()
            return True
        return False

    def update_game_turn(self, game_id: str, turn: int):
        """Update the turn of a game."""
        game = self.get_game_by_id(game_id)
        if game:
            game.turn = turn
            self.session.commit()
            return True
        return False

    def _generate_galaxy(self, game: Game, size: str):
        """Generate a galaxy with random star systems."""
        galaxy = Galaxy(game=game, size=size)
        
        # Determine number of star systems based on galaxy size
        if size == "small":
            num_systems = random.randint(10, 20)
        elif size == "medium":
            num_systems = random.randint(20, 40)
        else:  # large
            num_systems = random.randint(40, 60)
        
        # Generate star systems
        systems = []
        for _ in range(num_systems):
            system = self._generate_star_system(galaxy)
            systems.append(system)
        
        # Mark the first system as explored
        if systems:
            systems[0].explored = True
            systems[0].discovery_level = 6  # visited
            galaxy.explored_count = 1
        
        return galaxy

    def _generate_star_system(self, galaxy: Galaxy):
        """Generate a random star system in the galaxy."""
        # Generate random position within a circular galaxy
        radius = random.random()  # 0 to 1
        angle = random.random() * 2 * math.pi  # 0 to 2π
        
        # Convert polar coordinates to Cartesian and normalize to [0,1] range
        x = (radius * math.cos(angle) + 1) / 2  # Convert from [-1,1] to [0,1]
        y = (radius * math.sin(angle) + 1) / 2  # Convert from [-1,1] to [0,1]
        
        # Generate system name
        name = self._generate_star_system_name()
        
        # Create star system
        system = StarSystem(
            galaxy=galaxy,
            name=name,
            position_x=x,
            position_y=y
        )
        
        # Generate planets
        num_planets = random.randint(1, 8)
        for i in range(num_planets):
            self._generate_planet(system, i + 1)
        
        return system

    def _generate_star_system_name(self):
        """Generate a random star system name."""
        if random.random() < 0.7:  # 70% chance of a prefix-suffix name
            prefix = random.choice(STAR_NAME_PREFIXES)
            suffix = random.choice(STAR_NAME_SUFFIXES)
            return f"{prefix} {suffix}"
        else:  # 30% chance of a name with a number
            prefix = random.choice(STAR_NAME_PREFIXES)
            number = random.randint(1, 999)
            return f"{prefix}-{number}"

    def _generate_planet_name(self):
        """Generate a random planet name."""
        if random.random() < 0.6:  # 60% chance of a prefix-suffix name
            prefix = random.choice(PLANET_NAME_PREFIXES)
            suffix = random.choice(PLANET_NAME_SUFFIXES)
            return f"{prefix} {suffix}"
        else:  # 40% chance of a single name with a number
            suffix = random.choice(PLANET_NAME_SUFFIXES)
            number = random.randint(1, 9)
            return f"{suffix} {number}"

    def _generate_planet(self, system: StarSystem, position_in_system: int):
        """Generate a random planet in the star system."""
        # Planet type probabilities based on position
        if position_in_system <= 2:  # Inner planets
            planet_types = ["rocky", "terrestrial", "volcanic"]
            weights = [0.5, 0.3, 0.2]
        elif position_in_system <= 4:  # Middle planets
            planet_types = ["terrestrial", "oceanic", "desert", "jungle", "arctic"]
            weights = [0.3, 0.2, 0.2, 0.15, 0.15]
        else:  # Outer planets
            planet_types = ["gas_giant", "ice_giant", "arctic"]
            weights = [0.5, 0.4, 0.1]
        
        # Choose planet type based on weights
        planet_type = random.choices(planet_types, weights=weights, k=1)[0]
        
        # Planet size based on type
        if planet_type in ["gas_giant", "ice_giant"]:
            size = random.randint(7, 10)
        elif planet_type in ["terrestrial", "oceanic", "jungle"]:
            size = random.randint(4, 7)
        else:
            size = random.randint(1, 5)
        
        # Create planet
        planet = Planet(
            system=system,
            name=self._generate_planet_name(),
            type=planet_type,
            size=size
        )
        
        # Create planet resources
        resources = PlanetResources(
            planet=planet,
            organic=random.randint(0, 100),
            mineral=random.randint(0, 100),
            energy=random.randint(0, 100),
            exotics=random.randint(0, 100)
        )
        
        self.session.add(planet)
        self.session.add(resources)
        
        return planet