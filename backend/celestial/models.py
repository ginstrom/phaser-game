from django.db import models
from django.core.exceptions import ValidationError
from core.fields import FixedPointField

def validate_positive_orbit(value):
    if value < 1:
        raise ValidationError('Orbit must be a positive integer.')

class System(models.Model):
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
        if self.pk:  # Only validate orbits if the system has been saved
            # Count total orbits used
            used_orbits = set()
            
            # Check planets
            planet_orbits = self.planets.values_list('orbit', flat=True)
            used_orbits.update(planet_orbits)
            
            # Check asteroid belts
            asteroid_orbits = self.asteroid_belts.values_list('orbit', flat=True)
            used_orbits.update(asteroid_orbits)
            
            # Validate total number of orbits
            if len(used_orbits) > self.MAX_ORBITS:
                raise ValidationError(f'System cannot have more than {self.MAX_ORBITS} occupied orbits.')
            
            # Validate no duplicate orbits (should be handled by the set operation above, but double-checking)
            if len(used_orbits) < (len(planet_orbits) + len(asteroid_orbits)):
                raise ValidationError('Each orbit can only be occupied by one celestial body.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        self.clean()  # Run clean again after save to validate orbits

# Create your models here.

class Planet(models.Model):
    # System relationship
    system = models.ForeignKey(
        'System',
        on_delete=models.CASCADE,
        related_name='planets',
        help_text="The system this planet belongs to",
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

    class Meta:
        app_label = 'celestial'

class Star(models.Model):
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
    # System relationship
    system = models.ForeignKey(
        'System',
        on_delete=models.CASCADE,
        related_name='asteroid_belts',
        help_text="The system this asteroid belt belongs to",
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

    class Meta:
        app_label = 'celestial'
