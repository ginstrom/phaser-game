from .models import Game

def process(game: Game) -> Game:
    """
    Process the end of turn for a game.
    
    Args:
        game (Game): The game instance to process
        
    Returns:
        Game: The updated game instance
    """
    # Advance turn counter
    game.turn += 1
    game.save()
    
    return game 