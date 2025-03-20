"""Game initialization and setup module.

This module handles the creation and setup of new games, including:
- Galaxy generation with star systems
- Empire creation for human and computer players
- Initial game state setup
- Validation of game parameters

The module provides functions to create the initial game state and ensures
all required components are properly initialized.
"""

import logging
from django.db import transaction
from enum import Enum
from play.models import Player, Race, Empire, Game
from play import turn
from celestial.models import System, Star, Planet, AsteroidBelt

logger = logging.getLogger(__name__)

class GalaxySize(str, Enum):
    """Enumeration of available galaxy sizes and their properties.
    
    Each size determines the number of star systems in the galaxy:
    - TINY: 2 systems
    - SMALL: 5 systems
    - MEDIUM: 10 systems
    - LARGE: 15 systems
    """
    TINY = "tiny"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

    @classmethod
    def choices(cls):
        """Get list of valid galaxy size choices.
        
        Returns:
            list: List of valid galaxy size values
        """
        return [size.value for size in cls]

    @property
    def system_count(self):
        """Get the number of star systems for this galaxy size.
        
        Returns:
            int: Number of star systems
        """
        return GALAXY_SIZE_SYSTEM_COUNTS[self]

# Move system counts to a separate dict to keep the enum clean
GALAXY_SIZE_SYSTEM_COUNTS = {
    GalaxySize.TINY: 2,
    GalaxySize.SMALL: 5,
    GalaxySize.MEDIUM: 10,
    GalaxySize.LARGE: 15
}

def create_star_system(game, x, y):
    """Create a single star system at the specified coordinates.
    
    Args:
        game (Game): The game instance to create the system for
        x (int): X coordinate for the system
        y (int): Y coordinate for the system
        
    Returns:
        System: The created star system instance
    """
    logger.debug(f"Creating star system at coordinates ({x}, {y})")
    star = Star.objects.create(star_type=Star.StarType.YELLOW)
    system = System.objects.create(
        game=game,
        star=star,
        x=x,
        y=y
    )
    
    # Add a terran planet in orbit 1
    planet = Planet.objects.create(
        system=system,
        orbit=1,
        mineral_production=75,
        organic_production=75,
        radioactive_production=25,
        exotic_production=25,
        mineral_storage_capacity=150,
        organic_storage_capacity=150,
        radioactive_storage_capacity=100,
        exotic_storage_capacity=100
    )
    logger.debug(f"Created terran planet in orbit 1 of system {system.id}")
    
    # Add an asteroid belt in orbit 2
    belt = AsteroidBelt.objects.create(
        system=system,
        orbit=2,
        mineral_production=100,
        organic_production=25,
        radioactive_production=75,
        exotic_production=50
    )
    logger.debug(f"Created asteroid belt in orbit 2 of system {system.id}")
    
    return system

def create_star_systems(game, count):
    """Create the specified number of star systems for the game.
    
    Args:
        game (Game): The game instance to create systems for
        count (int): Number of star systems to create
        
    Returns:
        list: List of created System instances
        
    Note:
        Currently uses a simple placement algorithm with fixed spacing.
        Future versions may implement more sophisticated galaxy generation.
    """
    logger.info(f"Creating {count} star systems for game {game.id}")
    systems = []
    for i in range(count):
        x = i * 2
        y = i * 2
        system = create_star_system(game, x, y)
        systems.append(system)
    logger.info(f"Successfully created {len(systems)} star systems")
    return systems

def create_computer_empires(game, count, race):
    """Create the specified number of computer-controlled empires.
    
    Args:
        game (Game): The game instance to create empires for
        count (int): Number of computer empires to create
        race (Race): The race to use for the computer empires
        
    Returns:
        list: List of created Empire instances
    """
    logger.info(f"Creating {count} computer empires for game {game.id}")
    empires = []
    for i in range(count):
        player = Player.objects.create(player_type=Player.PlayerType.COMPUTER)
        empire = Empire.objects.create(
            name=f"Computer Empire {i+1}",
            player=player,
            race=race,
            game=game
        )
        empires.append(empire)
        logger.debug(f"Created computer empire {empire.name} with ID {empire.id}")
    logger.info(f"Successfully created {len(empires)} computer empires")
    return empires

def assign_colony_planets(game):
    """Assign colony planets to each empire in the game.
    
    If there are more empires than systems with planets, creates additional systems
    to ensure each empire gets its own colony planet.
    
    Args:
        game (Game): The game instance to assign colonies for
    """
    logger.info(f"Assigning colony planets for game {game.id}")
    empires = list(Empire.objects.filter(game=game))
    total_empires = len(empires)
    logger.debug(f"Found {total_empires} empires to assign colonies to")
    
    systems = list(System.objects.filter(game=game))
    total_systems = len(systems)
    logger.debug(f"Found {total_systems} existing systems")
    
    systems_needed = max(total_empires - total_systems, 0)
    if systems_needed > 0:
        logger.info(f"Creating {systems_needed} additional systems for colony assignment")
        for i in range(systems_needed):
            x = (total_systems + i) * 2
            y = (total_systems + i) * 2
            system = create_star_system(game, x, y)
            systems.append(system)
    
    for i, empire in enumerate(empires):
        system = systems[i]
        planet = system.planets.first()
        planet.empire = empire
        planet.save()
        logger.debug(f"Assigned planet {planet.id} in system {system.id} to empire {empire.name}")

@transaction.atomic
def start_game(data):
    """Initialize a new game with the specified parameters.
    
    This function handles the complete game initialization process:
    1. Creates a new game instance
    2. Generates the galaxy with star systems
    3. Creates the human player's empire
    4. Creates computer-controlled empires
    5. Assigns colony planets to each empire
    6. Validates the game state
    
    Args:
        data (dict): Dictionary containing:
            - player_empire_name (str): Name for the human player's empire
            - computer_empire_count (int): Number of computer empires
            - galaxy_size (str): Size of the galaxy (must be a valid GalaxySize value)
            
    Returns:
        Game: The newly created game instance
        
    Raises:
        ValueError: If galaxy_size is invalid or required fields are missing
        ValidationError: If game state is invalid after creation
    """
    logger.info("Starting new game initialization")
    
    # Validate required fields
    required_fields = ['player_empire_name', 'computer_empire_count', 'galaxy_size']
    for field in required_fields:
        if field not in data:
            logger.error(f"Missing required field: {field}")
            raise ValueError(f'Missing required field: {field}')

    # Validate and convert galaxy size
    try:
        galaxy_size = GalaxySize(data['galaxy_size'])
        logger.debug(f"Validated galaxy size: {galaxy_size}")
    except ValueError:
        logger.error(f"Invalid galaxy size: {data['galaxy_size']}")
        raise ValueError(f'Invalid galaxy size: {data["galaxy_size"]}')

    # Validate computer empire count
    if data['computer_empire_count'] < 0:
        logger.error(f"Invalid computer empire count: {data['computer_empire_count']}")
        raise ValueError('Computer empire count must be non-negative')

    # Get or create default race
    race, created = Race.objects.get_or_create(name="Human")
    if created:
        logger.info("Created new Human race")
    else:
        logger.debug("Using existing Human race")
    
    # Create game
    game = Game.objects.create(turn=0)
    logger.info(f"Created new game with ID {game.id}")
    
    # Create star systems based on galaxy size
    create_star_systems(game, GALAXY_SIZE_SYSTEM_COUNTS[galaxy_size])
    
    # Create human player and empire
    human_player = Player.objects.create(player_type=Player.PlayerType.HUMAN)
    human_empire = Empire.objects.create(
        name=data['player_empire_name'],
        player=human_player,
        race=race,
        game=game
    )
    logger.info(f"Created human empire '{human_empire.name}' with ID {human_empire.id}")
    
    # Create computer empires
    create_computer_empires(game, data['computer_empire_count'], race)
    
    # Assign colony planets to all empires
    assign_colony_planets(game)
    game = turn.process(game)
    
    logger.info(f"Successfully completed game initialization for game {game.id}")
    return game 