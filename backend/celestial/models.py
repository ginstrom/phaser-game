from django.db import models
from core.fields import FixedPointField

# Create your models here.

class Planet(models.Model):
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

    def __str__(self):
        return f"Asteroid Belt {self.id}"

    class Meta:
        app_label = 'celestial'
