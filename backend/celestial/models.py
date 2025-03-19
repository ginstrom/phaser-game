"""Celestial bodies and star systems for the space conquest game.

This module defines the core astronomical objects in the game:

**Models:**
- :model:`celestial.System`: Star systems with unique coordinates
- :model:`celestial.Star`: Stars of different types
- :model:`celestial.Planet`: Planets with resource production and storage
- :model:`celestial.AsteroidBelt`: Asteroid belts with resource production
"""

from django.db import models
from django.core.exceptions import ValidationError
from core.fields import FixedPointField

def validate_positive_orbit(value):
    """Ensure orbit numbers are positive integers.
    
    **Validation:**
    - Value must be greater than 0
    """
    if value < 1:
        raise ValidationError('Orbit must be a positive integer.')

class System(models.Model):
    """A star system in the game galaxy.
    
    **Relationships:**
    - One-to-one with :model:`celestial.Star`
    - Many-to-one with :model:`play.Game`
    - One-to-many with :model:`celestial.Planet`
    - One-to-many with :model:`celestial.AsteroidBelt`
    
    **Constraints:**
    - Maximum of 5 orbital positions
    - Unique x,y coordinates within a game
    - Each orbit can only be occupied by one celestial body
    """
    MAX_ORBITS = 5

    # Coordinates in the galaxy
    x = models.IntegerField(
        help_text="X coordinate in the galaxy"
    )
    y = models.IntegerField(
        help_text="Y coordinate in the galaxy"
    )

    # One-to-one relationship with Star
    star = models.OneToOneField(
        'Star',
        on_delete=models.CASCADE,
        related_name='system',
        help_text="The star at the center of this system"
    )

    # Game relationship
    game = models.ForeignKey(
        'play.Game',
        on_delete=models.CASCADE,
        related_name='systems',
        help_text="The game this system belongs to",
        null=True,
        blank=True
    )

    class Meta:
        app_label = 'celestial'
        unique_together = ['game', 'x', 'y']  # Ensure no two systems in the same game occupy the same position

    def __str__(self):
        return f"System at ({self.x}, {self.y})"

    def clean(self):
        """Validate orbital positions and total number of orbits.
        
        **Validation:**
        - Total number of orbits cannot exceed MAX_ORBITS
        - No duplicate orbital positions allowed
        """
        if self.pk:  # Only validate orbits if the system has been saved
            # Get all used orbits
            used_orbits = set()
            
            # Check planets
            planet_orbits = set(self.planets.values_list('orbit', flat=True))
            used_orbits.update(planet_orbits)
            
            # Check asteroid belts
            asteroid_orbits = set(self.asteroid_belts.values_list('orbit', flat=True))
            used_orbits.update(asteroid_orbits)
            
            # Validate total number of orbits
            if len(used_orbits) > self.MAX_ORBITS:
                raise ValidationError(f'System cannot have more than {self.MAX_ORBITS} occupied orbits.')
            
            # Validate no duplicate orbits between planets and asteroid belts
            if planet_orbits & asteroid_orbits:  # Check for intersection
                raise ValidationError('Each orbit can only be occupied by one celestial body.')

    def save(self, *args, **kwargs):
        """Save the system and validate orbital positions.
        
        **Process:**
        1. Save to database
        2. Run clean() to validate relationships
        """
        super().save(*args, **kwargs)
        self.clean()  # Run clean after save to validate orbits

# Create your models here.

class Planet(models.Model):
    """A planet in a star system.
    
    **Relationships:**
    - Many-to-one with :model:`celestial.System`
    - Many-to-one with :model:`play.Empire` (owner)
    
    **Fields:**
    - Resource production rates (mineral, organic, radioactive, exotic)
    - Resource storage capacities
    - Orbital position
    """
    # System relationship
    system = models.ForeignKey(
        'System',
        on_delete=models.CASCADE,
        related_name='planets',
        help_text="The system this planet belongs to",
        null=True,
        blank=True
    )

    # Empire relationship (owner)
    empire = models.ForeignKey(
        'play.Empire',
        on_delete=models.SET_NULL,
        related_name='owned_planets',
        help_text="The empire that owns this planet",
        null=True,
        blank=True
    )

    # Resource Production Fields
    mineral_production = FixedPointField(
        default=50,
        help_text="Base mineral production per turn"
    )
    organic_production = FixedPointField(
        default=50,
        help_text="Base organic production per turn"
    )
    radioactive_production = FixedPointField(
        default=50,
        help_text="Base radioactive production per turn"
    )
    exotic_production = FixedPointField(
        default=50,
        help_text="Base exotic production per turn"
    )

    # Resource Storage Capacity Fields
    mineral_storage_capacity = FixedPointField(
        default=100,
        help_text="Maximum mineral storage capacity"
    )
    organic_storage_capacity = FixedPointField(
        default=100,
        help_text="Maximum organic storage capacity"
    )
    radioactive_storage_capacity = FixedPointField(
        default=100,
        help_text="Maximum radioactive storage capacity"
    )
    exotic_storage_capacity = FixedPointField(
        default=100,
        help_text="Maximum exotic storage capacity"
    )

    # Orbital Position
    orbit = models.PositiveIntegerField(
        default=1,
        help_text="The orbital position from the star (1 being closest)",
        validators=[validate_positive_orbit]
    )

    def __str__(self):
        return f"Planet {self.id}"

    def clean(self):
        """Validate orbital position.
        
        **Validation:**
        - Orbit must be unique within the system
        - Orbit cannot be shared with asteroid belts
        """
        if self.system and self.orbit:
            # Check for other planets in the same orbit
            if Planet.objects.filter(system=self.system, orbit=self.orbit).exclude(pk=self.pk).exists():
                raise ValidationError(f'Orbit {self.orbit} is already occupied by another planet in this system.')
            
            # Check for asteroid belts in the same orbit
            if AsteroidBelt.objects.filter(system=self.system, orbit=self.orbit).exists():
                raise ValidationError(f'Orbit {self.orbit} is already occupied by an asteroid belt in this system.')

    def save(self, *args, **kwargs):
        """Save the planet and validate orbital position."""
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'celestial'

class Star(models.Model):
    """A star at the center of a star system.
    
    **Relationships:**
    - One-to-one with :model:`celestial.System`
    
    **Types:**
    - Blue
    - White
    - Yellow
    - Orange
    - Brown
    """
    class StarType(models.TextChoices):
        BLUE = 'blue', 'Blue'
        WHITE = 'white', 'White'
        YELLOW = 'yellow', 'Yellow'
        ORANGE = 'orange', 'Orange'
        BROWN = 'brown', 'Brown'

    star_type = models.CharField(
        max_length=10,
        choices=StarType.choices,
        help_text="The type of star"
    )

    def __str__(self):
        return f"{self.star_type.capitalize()} Star {self.id}"

    class Meta:
        app_label = 'celestial'

class AsteroidBelt(models.Model):
    """An asteroid belt in a star system.
    
    **Relationships:**
    - Many-to-one with :model:`celestial.System`
    - Many-to-one with :model:`play.Empire` (owner)
    
    **Fields:**
    - Resource production rates (mineral, organic, radioactive, exotic)
    - Orbital position
    """
    # System relationship
    system = models.ForeignKey(
        'System',
        on_delete=models.CASCADE,
        related_name='asteroid_belts',
        help_text="The system this asteroid belt belongs to",
        null=True,
        blank=True
    )

    # Empire relationship (owner)
    empire = models.ForeignKey(
        'play.Empire',
        on_delete=models.SET_NULL,
        related_name='owned_asteroid_belts',
        help_text="The empire that owns this asteroid belt",
        null=True,
        blank=True
    )

    # Resource Production Fields
    mineral_production = FixedPointField(
        default=50,
        help_text="Base mineral production per turn"
    )
    organic_production = FixedPointField(
        default=50,
        help_text="Base organic production per turn"
    )
    radioactive_production = FixedPointField(
        default=50,
        help_text="Base radioactive production per turn"
    )
    exotic_production = FixedPointField(
        default=50,
        help_text="Base exotic production per turn"
    )

    # Orbital Position
    orbit = models.PositiveIntegerField(
        default=1,
        help_text="The orbital position from the star (1 being closest)",
        validators=[validate_positive_orbit]
    )

    def __str__(self):
        return f"Asteroid Belt {self.id}"

    def clean(self):
        """Validate orbital position.
        
        **Validation:**
        - Orbit must be unique within the system
        - Orbit cannot be shared with planets
        """
        if self.system and self.orbit:
            # Check for planets in the same orbit
            if Planet.objects.filter(system=self.system, orbit=self.orbit).exists():
                raise ValidationError(f'Orbit {self.orbit} is already occupied by a planet in this system.')
            
            # Check for other asteroid belts in the same orbit
            if AsteroidBelt.objects.filter(system=self.system, orbit=self.orbit).exclude(pk=self.pk).exists():
                raise ValidationError(f'Orbit {self.orbit} is already occupied by another asteroid belt in this system.')

    def save(self, *args, **kwargs):
        """Save the asteroid belt and validate orbital position."""
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'celestial'
