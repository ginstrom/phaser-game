from decimal import Decimal
from django.test import TestCase
from django.db import models
from core.fields import FixedPointField
from celestial.models import Planet


class FixedPointFieldTests(TestCase):
    def test_init_default_scale(self):
        """Test that FixedPointField initializes with default scale"""
        field = FixedPointField()
        self.assertEqual(field.scale, 1000)

    def test_init_custom_scale(self):
        """Test that FixedPointField accepts custom scale"""
        field = FixedPointField(scale=10000)
        self.assertEqual(field.scale, 10000)

    def test_to_python(self):
        """Test conversion of various types to Python Decimal"""
        field = FixedPointField()
        
        # Test None value
        self.assertIsNone(field.to_python(None))
        
        # Test Decimal value
        decimal_value = Decimal('1.234')
        self.assertEqual(field.to_python(decimal_value), decimal_value)
        
        # Test string value
        self.assertEqual(field.to_python('1234'), Decimal('1.234'))
        
        # Test integer value
        self.assertEqual(field.to_python(1234), Decimal('1.234'))
        
        # Test invalid value
        with self.assertRaises(ValueError):
            field.to_python('invalid')

    def test_get_prep_value(self):
        """Test conversion of Python value to database value"""
        field = FixedPointField()
        
        # Test None value
        self.assertIsNone(field.get_prep_value(None))
        
        # Test decimal value
        self.assertEqual(field.get_prep_value(Decimal('1.234')), 1234)
        
        # Test negative value
        self.assertEqual(field.get_prep_value(Decimal('-1.234')), -1234)
        
        # Test zero
        self.assertEqual(field.get_prep_value(Decimal('0')), 0)

    def test_from_db_value(self):
        """Test conversion from database value to Python value"""
        field = FixedPointField()
        
        # Test None value
        self.assertIsNone(field.from_db_value(None, None, None))
        
        # Test positive integer
        self.assertEqual(field.from_db_value(1234, None, None), Decimal('1.234'))
        
        # Test negative integer
        self.assertEqual(field.from_db_value(-1234, None, None), Decimal('-1.234'))
        
        # Test zero
        self.assertEqual(field.from_db_value(0, None, None), Decimal('0'))

    def test_deconstruct(self):
        """Test field deconstruction for migrations"""
        field = FixedPointField(scale=10000)
        name, path, args, kwargs = field.deconstruct()
        
        self.assertEqual(kwargs['scale'], 10000)
        
        # Default scale should not be in kwargs
        field = FixedPointField()
        name, path, args, kwargs = field.deconstruct()
        self.assertNotIn('scale', kwargs)

    def test_database_storage(self):
        """Test actual database storage and retrieval"""
        # Create test planet
        planet = Planet.objects.create(
            mineral_production=Decimal('1.234'),
            mineral_storage_capacity=Decimal('1.234')
        )
        
        # Retrieve from database
        planet = Planet.objects.get(pk=planet.pk)
        
        # Check regular scale field
        self.assertEqual(planet.mineral_production, Decimal('1.234'))
        
        # Check storage capacity field
        self.assertEqual(planet.mineral_storage_capacity, Decimal('1.234'))

    def test_rounding(self):
        """Test handling of values that exceed scale precision"""
        planet = Planet(
            mineral_production=Decimal('1.2345'),  # More precise than scale=1000
            mineral_storage_capacity=Decimal('1.2345')  # More precise than scale=1000
        )
        
        # Save should not raise any errors
        planet.save()
        
        # Retrieve and check values
        planet = Planet.objects.get(pk=planet.pk)
        
        # Should be truncated to scale precision
        self.assertEqual(planet.mineral_production, Decimal('1.234'))
        self.assertEqual(planet.mineral_storage_capacity, Decimal('1.234')) 