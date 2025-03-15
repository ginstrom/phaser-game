"""
Test cases for celestial models.
"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal
from ..models import Planet, Star


class PlanetModelTest(TestCase):
    def test_create_planet_default_values(self):
        """Test creating a planet with default values"""
        planet = Planet.objects.create()
        
        # Test production values
        self.assertEqual(planet.mineral_production, Decimal('50'))
        self.assertEqual(planet.organic_production, Decimal('50'))
        self.assertEqual(planet.radioactive_production, Decimal('50'))
        self.assertEqual(planet.exotic_production, Decimal('50'))
        
        # Test storage capacity values
        self.assertEqual(planet.mineral_storage_capacity, Decimal('100'))
        self.assertEqual(planet.organic_storage_capacity, Decimal('100'))
        self.assertEqual(planet.radioactive_storage_capacity, Decimal('100'))
        self.assertEqual(planet.exotic_storage_capacity, Decimal('100'))

    def test_create_planet_custom_values(self):
        """Test creating a planet with custom values"""
        planet = Planet.objects.create(
            mineral_production=Decimal('75.5'),
            organic_production=Decimal('25.25'),
            radioactive_production=Decimal('60.75'),
            exotic_production=Decimal('40.25'),
            mineral_storage_capacity=Decimal('150.5'),
            organic_storage_capacity=Decimal('200.75'),
            radioactive_storage_capacity=Decimal('175.25'),
            exotic_storage_capacity=Decimal('125.75')
        )
        
        # Test production values
        self.assertEqual(planet.mineral_production, Decimal('75.5'))
        self.assertEqual(planet.organic_production, Decimal('25.25'))
        self.assertEqual(planet.radioactive_production, Decimal('60.75'))
        self.assertEqual(planet.exotic_production, Decimal('40.25'))
        
        # Test storage capacity values
        self.assertEqual(planet.mineral_storage_capacity, Decimal('150.5'))
        self.assertEqual(planet.organic_storage_capacity, Decimal('200.75'))
        self.assertEqual(planet.radioactive_storage_capacity, Decimal('175.25'))
        self.assertEqual(planet.exotic_storage_capacity, Decimal('125.75'))

    def test_string_representation(self):
        """Test the string representation of a Planet"""
        planet = Planet.objects.create()
        self.assertEqual(str(planet), f"Planet {planet.id}")

    def test_field_precision(self):
        """Test that fields maintain their decimal precision"""
        test_value = Decimal('42.125')  # Test with 3 decimal places
        planet = Planet.objects.create(mineral_production=test_value)
        
        # Refresh from database to ensure we test what's actually stored
        planet.refresh_from_db()
        self.assertEqual(planet.mineral_production, test_value)

class StarModelTest(TestCase):
    def test_create_star(self):
        """Test creating a star with valid type"""
        star = Star.objects.create(star_type='blue')
        self.assertEqual(star.star_type, 'blue')
        self.assertEqual(str(star), 'Blue Star 1')

    def test_create_star_invalid_type(self):
        """Test creating a star with invalid type raises error"""
        with self.assertRaises(ValidationError):
            star = Star(star_type='invalid')
            star.full_clean()

    def test_star_types_exist(self):
        """Test all required star types are available"""
        expected_types = {'blue', 'white', 'yellow', 'orange', 'brown'}
        actual_types = {choice[0] for choice in Star.StarType.choices}
        self.assertEqual(expected_types, actual_types) 