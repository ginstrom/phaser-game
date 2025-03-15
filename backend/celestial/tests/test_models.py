"""
Test cases for celestial models.
"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal
from ..models import Planet, Star, AsteroidBelt


class PlanetModelTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.default_planet = Planet.objects.create()
        self.custom_planet = Planet.objects.create(
            mineral_production=Decimal('75.5'),
            organic_production=Decimal('25.25'),
            radioactive_production=Decimal('60.75'),
            exotic_production=Decimal('40.25'),
            mineral_storage_capacity=Decimal('150.5'),
            organic_storage_capacity=Decimal('200.75'),
            radioactive_storage_capacity=Decimal('175.25'),
            exotic_storage_capacity=Decimal('125.75'),
            orbit=3
        )

    def tearDown(self):
        """Clean up test data"""
        Planet.objects.all().delete()

    def test_create_planet_default_values(self):
        """Test creating a planet with default values"""
        planet = self.default_planet
        
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

        # Test orbit value
        self.assertEqual(planet.orbit, 1)

    def test_create_planet_custom_values(self):
        """Test creating a planet with custom values"""
        planet = self.custom_planet
        
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

        # Test orbit value
        self.assertEqual(planet.orbit, 3)

    def test_string_representation(self):
        """Test the string representation of a Planet"""
        planet = self.default_planet
        self.assertEqual(str(planet), f"Planet {planet.id}")

    def test_field_precision(self):
        """Test that fields maintain their decimal precision"""
        test_value = Decimal('42.125')  # Test with 3 decimal places
        planet = Planet.objects.create(mineral_production=test_value)
        
        # Refresh from database to ensure we test what's actually stored
        planet.refresh_from_db()
        self.assertEqual(planet.mineral_production, test_value)

    def test_negative_orbit_validation(self):
        """Test that negative orbit values are not allowed"""
        planet = Planet(orbit=-1)
        with self.assertRaises(ValidationError):
            planet.full_clean()


class StarModelTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.star = Star.objects.create(star_type='blue')

    def tearDown(self):
        """Clean up test data"""
        Star.objects.all().delete()

    def test_create_star(self):
        """Test creating a star with valid type"""
        self.assertEqual(self.star.star_type, 'blue')
        self.assertEqual(str(self.star), f'Blue Star {self.star.id}')

    def test_invalid_star_type(self):
        """Test creating a star with invalid type"""
        with self.assertRaises(ValidationError):
            star = Star(star_type='invalid')
            star.full_clean()


class AsteroidBeltModelTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.default_belt = AsteroidBelt.objects.create()
        self.custom_belt = AsteroidBelt.objects.create(
            mineral_production=Decimal('75.5'),
            organic_production=Decimal('25.25'),
            radioactive_production=Decimal('60.75'),
            exotic_production=Decimal('40.25'),
            orbit=4
        )

    def tearDown(self):
        """Clean up test data"""
        AsteroidBelt.objects.all().delete()

    def test_create_asteroid_belt_default_values(self):
        """Test creating an asteroid belt with default values"""
        belt = self.default_belt
        
        # Test production values
        self.assertEqual(belt.mineral_production, Decimal('50'))
        self.assertEqual(belt.organic_production, Decimal('50'))
        self.assertEqual(belt.radioactive_production, Decimal('50'))
        self.assertEqual(belt.exotic_production, Decimal('50'))

        # Test orbit value
        self.assertEqual(belt.orbit, 1)

    def test_create_asteroid_belt_custom_values(self):
        """Test creating an asteroid belt with custom values"""
        belt = self.custom_belt
        
        # Test production values
        self.assertEqual(belt.mineral_production, Decimal('75.5'))
        self.assertEqual(belt.organic_production, Decimal('25.25'))
        self.assertEqual(belt.radioactive_production, Decimal('60.75'))
        self.assertEqual(belt.exotic_production, Decimal('40.25'))

        # Test orbit value
        self.assertEqual(belt.orbit, 4)

    def test_string_representation(self):
        """Test the string representation of an AsteroidBelt"""
        belt = self.default_belt
        self.assertEqual(str(belt), f"Asteroid Belt {belt.id}")

    def test_field_precision(self):
        """Test that fields maintain their decimal precision"""
        test_value = Decimal('42.125')  # Test with 3 decimal places
        belt = AsteroidBelt.objects.create(mineral_production=test_value)
        
        # Refresh from database to ensure we test what's actually stored
        belt.refresh_from_db()
        self.assertEqual(belt.mineral_production, test_value)

    def test_negative_orbit_validation(self):
        """Test that negative orbit values are not allowed"""
        belt = AsteroidBelt(orbit=-1)
        with self.assertRaises(ValidationError):
            belt.full_clean() 