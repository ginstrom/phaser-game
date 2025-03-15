from decimal import Decimal
from django.test import TestCase
from django.db import models
from core.fields import FixedPointField


# Test model that uses FixedPointField
class TestModel(models.Model):
    value = FixedPointField()
    custom_scale = FixedPointField(scale=10000)

    class Meta:
        app_label = 'core'


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
        # Create test instances
        TestModel.objects.create(
            value=Decimal('1.234'),
            custom_scale=Decimal('1.2345')
        )
        
        # Retrieve from database
        instance = TestModel.objects.get()
        
        # Check regular scale field
        self.assertEqual(instance.value, Decimal('1.234'))
        
        # Check custom scale field
        self.assertEqual(instance.custom_scale, Decimal('1.2345'))

    def test_rounding(self):
        """Test handling of values that exceed scale precision"""
        instance = TestModel(
            value=Decimal('1.2345'),  # More precise than scale=1000
            custom_scale=Decimal('1.23456')  # More precise than scale=10000
        )
        
        # Save should not raise any errors
        instance.save()
        
        # Retrieve and check values
        instance = TestModel.objects.get(pk=instance.pk)
        
        # Should be truncated to scale precision
        self.assertEqual(instance.value, Decimal('1.234'))
        self.assertEqual(instance.custom_scale, Decimal('1.2345')) 