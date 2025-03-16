from django.db import transaction
from play.models import Player, Race, Empire, Game
from celestial.models import System, Star

class GalaxySize:
    TINY = "tiny"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

    SYSTEM_COUNTS = {
        TINY: 2,
        SMALL: 5,
        MEDIUM: 10,
        LARGE: 15
    }

def create_star_systems(game, count):
    """Create the specified number of star systems for the game"""
    systems = []
    for i in range(count):
        # Simple placement - can be improved with more sophisticated algorithms
        x = i * 2  # Simple spacing
        y = i * 2
        star = Star.objects.create(star_type=Star.StarType.YELLOW)
        system = System.objects.create(
            game=game,
            star=star,
            x=x,
            y=y
        )
        systems.append(system)
    return systems

def create_computer_empires(game, count, race):
    """Create the specified number of computer empires"""
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
    """
    Initialize a new game with the specified parameters
    
    Args:
        data (dict): Dictionary containing:
            - player_empire_name (str): Name for the human player's empire
            - computer_empire_count (int): Number of computer empires
            - galaxy_size (str): One of 'tiny', 'small', 'medium', 'large'
            
    Returns:
        Game: The newly created game instance
    """
    # Validate galaxy size
    galaxy_size = data['galaxy_size'].lower()
    if galaxy_size not in GalaxySize.SYSTEM_COUNTS:
        raise ValueError(f"Invalid galaxy size: {galaxy_size}")
    
    # Get or create default race (can be expanded later)
    race, _ = Race.objects.get_or_create(name="Human")
    
    # Create game
    game = Game.objects.create(turn=1)
    
    # Create star systems based on galaxy size
    system_count = GalaxySize.SYSTEM_COUNTS[galaxy_size]
    create_star_systems(game, system_count)
    
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