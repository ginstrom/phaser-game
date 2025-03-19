"""Game initialization and setup module.

This module handles the creation and setup of new games, including:
- Galaxy generation with star systems
- Empire creation for human and computer players
- Initial game state setup
- Validation of game parameters

The module provides functions to create the initial game state and ensures
all required components are properly initialized.
"""

from django.db import transaction
from enum import Enum
from play.models import Player, Race, Empire, Game
from celestial.models import System, Star

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
    star = Star.objects.create(star_type=Star.StarType.YELLOW)
    system = System.objects.create(
        game=game,
        star=star,
        x=x,
        y=y
    )
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
    systems = []
    for i in range(count):
        # Simple placement - can be improved with more sophisticated algorithms
        x = i * 2  # Simple spacing
        y = i * 2
        system = create_star_system(game, x, y)
        systems.append(system)
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
    return empires

@transaction.atomic
def start_game(data):
    """Initialize a new game with the specified parameters.
    
    This function handles the complete game initialization process:
    1. Creates a new game instance
    2. Generates the galaxy with star systems
    3. Creates the human player's empire
    4. Creates computer-controlled empires
    5. Validates the game state
    
    Args:
        data (dict): Dictionary containing:
            - player_empire_name (str): Name for the human player's empire
            - computer_empire_count (int): Number of computer empires
            - galaxy_size (GalaxySize): Size of the galaxy
            
    Returns:
        Game: The newly created game instance
        
    Raises:
        ValueError: If galaxy_size is invalid
        ValidationError: If game state is invalid after creation
    """
    # Get or create default race (can be expanded later)
    race, _ = Race.objects.get_or_create(name="Human")
    
    # Create game
    game = Game.objects.create(turn=0)
    
    # Create star systems based on galaxy size
    galaxy_size = data['galaxy_size']
    create_star_systems(game, galaxy_size.system_count)
    
    # Create human player and empire
    human_player = Player.objects.create(player_type=Player.PlayerType.HUMAN)
    human_empire = Empire.objects.create(
        name=data['player_empire_name'],
        player=human_player,
        race=race,
        game=game
    )
    
    # Create computer empires
    create_computer_empires(game, data['computer_empire_count'], race)
    
    # Validate game (ensures minimum requirements are met)
    game.clean()
    
    return game 