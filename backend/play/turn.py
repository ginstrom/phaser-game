"""Turn processing module for the space conquest game.

This module handles the end-of-turn processing for games, including:
- Advancing the turn counter
- Persisting game state changes
- Triggering any turn-based events or updates
- Calculating resource production and storage

The module provides a single public function `process()` that handles all turn processing logic.
"""

import logging
from .models import Game, Empire
from celestial.models import Planet, AsteroidBelt
from decimal import Decimal
from django.db.models import Sum

logger = logging.getLogger(__name__)

def calculate_resource_production(empire: Empire) -> tuple[Decimal, Decimal, Decimal, Decimal]:
    """Calculate total resource production for an empire from all its planets and asteroid belts.
    
    Args:
        empire (Empire): The empire to calculate production for
        
    Returns:
        tuple[Decimal, Decimal, Decimal, Decimal]: Total production of (mineral, organic, radioactive, exotic)
    """
    logger.debug(f"Calculating resource production for empire {empire.name} (ID: {empire.id})")
    
    # Sum production from planets
    planet_prod = empire.planets.aggregate(
        mineral_prod=Sum('mineral_production'),
        organic_prod=Sum('organic_production'),
        radioactive_prod=Sum('radioactive_production'),
        exotic_prod=Sum('exotic_production')
    )
    
    # Sum production from asteroid belts
    belt_prod = empire.asteroid_belts.aggregate(
        mineral_prod=Sum('mineral_production'),
        organic_prod=Sum('organic_production'),
        radioactive_prod=Sum('radioactive_production'),
        exotic_prod=Sum('exotic_production')
    )
    
    # Combine planet and belt production, handling None values
    mineral_prod = (planet_prod['mineral_prod'] or Decimal('0')) + (belt_prod['mineral_prod'] or Decimal('0'))
    organic_prod = (planet_prod['organic_prod'] or Decimal('0')) + (belt_prod['organic_prod'] or Decimal('0'))
    radioactive_prod = (planet_prod['radioactive_prod'] or Decimal('0')) + (belt_prod['radioactive_prod'] or Decimal('0'))
    exotic_prod = (planet_prod['exotic_prod'] or Decimal('0')) + (belt_prod['exotic_prod'] or Decimal('0'))
    
    logger.debug(f"Resource production for empire {empire.name}: "
                f"Mineral={mineral_prod}, Organic={organic_prod}, "
                f"Radioactive={radioactive_prod}, Exotic={exotic_prod}")
    
    return mineral_prod, organic_prod, radioactive_prod, exotic_prod

def update_empire_resources(empire: Empire) -> None:
    """Update an empire's resource storage based on production and capacity.
    
    Args:
        empire (Empire): The empire to update resources for
    """
    logger.debug(f"Updating resources for empire {empire.name} (ID: {empire.id})")
    
    # Get total production
    mineral_prod, organic_prod, radioactive_prod, exotic_prod = calculate_resource_production(empire)
    
    # Store old values for logging
    old_mineral = empire.mineral_storage
    old_organic = empire.organic_storage
    old_radioactive = empire.radioactive_storage
    old_exotic = empire.exotic_storage
    
    # Update storage values, capped at capacity
    empire.mineral_storage = min(empire.mineral_storage + mineral_prod, empire.mineral_capacity)
    empire.organic_storage = min(empire.organic_storage + organic_prod, empire.organic_capacity)
    empire.radioactive_storage = min(empire.radioactive_storage + radioactive_prod, empire.radioactive_capacity)
    empire.exotic_storage = min(empire.exotic_storage + exotic_prod, empire.exotic_capacity)
    
    # Save changes
    empire.save()
    
    logger.debug(f"Resource storage updated for empire {empire.name}: "
                f"Mineral: {old_mineral} -> {empire.mineral_storage}, "
                f"Organic: {old_organic} -> {empire.organic_storage}, "
                f"Radioactive: {old_radioactive} -> {empire.radioactive_storage}, "
                f"Exotic: {old_exotic} -> {empire.exotic_storage}")

def process(game: Game) -> Game:
    """Process the end of turn for a game.
    
    This function handles all end-of-turn processing for a game, including:
    - Advancing the turn counter
    - Calculating resource production for each empire
    - Updating resource storage values
    - Saving the updated game state
    
    Args:
        game (Game): The game instance to process
        
    Returns:
        Game: The updated game instance with the turn counter advanced
    """
    logger.info(f"Processing end of turn {game.turn} for game {game.id}")
    
    # Process resources for each empire
    empires = game.empires.all()
    logger.info(f"Processing resources for {len(empires)} empires")
    
    for empire in empires:
        update_empire_resources(empire)
    
    # Advance turn counter
    old_turn = game.turn
    game.turn += 1
    game.save()
    
    logger.info(f"Turn processing complete. Game {game.id} advanced from turn {old_turn} to {game.turn}")
    return game 