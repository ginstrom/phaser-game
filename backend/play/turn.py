"""Turn processing module for the space conquest game.

This module handles the end-of-turn processing for games, including:
- Advancing the turn counter
- Persisting game state changes
- Triggering any turn-based events or updates

The module provides a single public function `process()` that handles all turn processing logic.
"""

from .models import Game

def process(game: Game) -> Game:
    """Process the end of turn for a game.
    
    This function handles all end-of-turn processing for a game, including:
    - Advancing the turn counter
    - Saving the updated game state
    
    Args:
        game (Game): The game instance to process
        
    Returns:
        Game: The updated game instance with the turn counter advanced
        
    Note:
        This is currently a simple implementation that only advances the turn counter.
        Future versions may include additional turn processing logic such as:
        - Resource production
        - Research progress
        - Fleet movements
        - Combat resolution
    """
    # Advance turn counter
    game.turn += 1
    game.save()
    
    return game 