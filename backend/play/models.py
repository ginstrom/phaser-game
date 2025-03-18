"""Core game models for the space conquest game.

This module defines the core data models for the game, including:
- Players (human and computer)
- Races (species/empire types)
- Empires (player-controlled factions)
- Games (game sessions)

These models form the foundation of the game's data structure and business logic.
"""

from django.db import models
from django.core.exceptions import ValidationError
from celestial.models import Planet, AsteroidBelt, System

# Create your models here.

class Player(models.Model):
    """Represents a player in the game, either human or computer controlled.
    
    Attributes:
        player_type (str): The type of player, either 'human' or 'computer'
    """
    class PlayerType(models.TextChoices):
        HUMAN = 'human', 'Human'
        COMPUTER = 'computer', 'Computer'

    player_type = models.CharField(
        max_length=10,
        choices=PlayerType.choices,
        default=PlayerType.HUMAN,
    )

    def __str__(self):
        return f"{self.player_type} player ({self.id})"

    class Meta:
        app_label = 'play'

class Race(models.Model):
    """Represents a species or empire type in the game.
    
    Attributes:
        name (str): The name of the race
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'play'

class Empire(models.Model):
    """Represents a player-controlled faction in the game.
    
    An empire is the main organizational unit for players, containing:
    - Resources and storage
    - Controlled planets and asteroid belts
    - Player and race associations
    
    Attributes:
        name (str): The name of the empire
        player (Player): The player controlling this empire
        race (Race): The race/species of this empire
        game (Game): The game this empire belongs to
        planets (ManyToManyField): The planets controlled by this empire
        asteroid_belts (ManyToManyField): The asteroid belts controlled by this empire
        mineral_storage (int): Current mineral resource storage
        organic_storage (int): Current organic resource storage
        radioactive_storage (int): Current radioactive resource storage
        exotic_storage (int): Current exotic resource storage
    """
    name = models.CharField(max_length=100)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='empires')
    race = models.ForeignKey(Race, on_delete=models.PROTECT, related_name='empires')
    game = models.ForeignKey(
        'Game',
        on_delete=models.CASCADE,
        related_name='empires',
        help_text="The game this empire belongs to",
        null=True,
        blank=True
    )
    planets = models.ManyToManyField(Planet, related_name='empire', blank=True)
    asteroid_belts = models.ManyToManyField(AsteroidBelt, related_name='empire', blank=True)
    
    # Resource storage values
    mineral_storage = models.IntegerField(default=0)
    organic_storage = models.IntegerField(default=0)
    radioactive_storage = models.IntegerField(default=0)
    exotic_storage = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.race.name})"

    @property
    def mineral_capacity(self):
        """Calculate total mineral storage capacity from all controlled planets.
        
        Returns:
            int: Total mineral storage capacity
        """
        return sum(planet.mineral_storage_capacity for planet in self.planets.all())

    @property
    def organic_capacity(self):
        """Calculate total organic storage capacity from all controlled planets.
        
        Returns:
            int: Total organic storage capacity
        """
        return sum(planet.organic_storage_capacity for planet in self.planets.all())

    @property
    def radioactive_capacity(self):
        """Calculate total radioactive storage capacity from all controlled planets.
        
        Returns:
            int: Total radioactive storage capacity
        """
        return sum(planet.radioactive_storage_capacity for planet in self.planets.all())

    @property
    def exotic_capacity(self):
        """Calculate total exotic storage capacity from all controlled planets.
        
        Returns:
            int: Total exotic storage capacity
        """
        return sum(planet.exotic_storage_capacity for planet in self.planets.all())

    class Meta:
        app_label = 'play'

class Game(models.Model):
    """Represents a game session in the space conquest game.
    
    A game contains:
    - Turn counter
    - Associated empires
    - Star systems
    - Game state validation rules
    
    Attributes:
        turn (int): Current turn number of the game
    """
    turn = models.PositiveIntegerField(
        default=0,
        help_text="Current turn number of the game"
    )

    def clean(self):
        """Validate that game meets minimum requirements.
        
        Ensures that:
        - Game has at least 2 empires
        - Game has at least 2 star systems
        
        Raises:
            ValidationError: If minimum requirements are not met
        """
        # Validate minimum number of empires
        if self.empires.count() < 2:
            raise ValidationError('Game must have at least 2 empires.')
        
        # Validate minimum number of systems
        if self.systems.count() < 2:
            raise ValidationError('Game must have at least 2 star systems.')

    def __str__(self):
        return f"Game {self.id} (Turn {self.turn})"

    class Meta:
        app_label = 'play'
