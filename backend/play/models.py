from django.db import models
from django.core.exceptions import ValidationError
from celestial.models import Planet, AsteroidBelt, System

# Create your models here.

class Player(models.Model):
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
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'play'

class Empire(models.Model):
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
        """Total mineral capacity from all planets"""
        return sum(planet.mineral_storage_capacity for planet in self.planets.all())

    @property
    def organic_capacity(self):
        """Total organic capacity from all planets"""
        return sum(planet.organic_storage_capacity for planet in self.planets.all())

    @property
    def radioactive_capacity(self):
        """Total radioactive capacity from all planets"""
        return sum(planet.radioactive_storage_capacity for planet in self.planets.all())

    @property
    def exotic_capacity(self):
        """Total exotic capacity from all planets"""
        return sum(planet.exotic_storage_capacity for planet in self.planets.all())

    class Meta:
        app_label = 'play'

class Game(models.Model):
    turn = models.PositiveIntegerField(
        default=1,
        help_text="Current turn number of the game"
    )

    def clean(self):
        """Validate that game has minimum required empires and systems"""
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
