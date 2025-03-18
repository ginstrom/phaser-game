"""Custom Django model fields for the game.

This module provides specialized field types for handling game-specific data:

**Fields:**
- :field:`core.FixedPointField`: Stores decimal numbers as integers to avoid floating point errors
"""

from django.db import models
from decimal import Decimal, InvalidOperation


class FixedPointField(models.IntegerField):
    """A field that stores decimal numbers as integers with a scale factor.
    
    This field avoids floating point errors by storing decimal values as integers
    with a configurable scale factor.
    
    **Example:**
    With scale=1000:
    - 1.234 is stored as 1234
    - 0.001 is stored as 1
    
    **Usage:**
    .. code-block:: python
        class MyModel(models.Model):
            value = FixedPointField(scale=1000)
    """
    description = "Fixed-point decimal number stored as an integer"

    def __init__(self, scale=1000, *args, **kwargs):
        """Initialize the field with a scale factor.
        
        **Args:**
            scale: Number to multiply by when storing (default: 1000)
        """
        self.scale = scale
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        """Return field parameters for model migrations.
        
        **Returns:**
            Tuple of (name, path, args, kwargs) for migration serialization
        """
        name, path, args, kwargs = super().deconstruct()
        if self.scale != 1000:
            kwargs['scale'] = self.scale
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection):
        """Convert database integer to decimal value.
        
        **Args:**
            value: Integer value from database
            expression: The expression that generated this value
            connection: The database connection
            
        **Returns:**
            Decimal value scaled by 1/scale
        """
        if value is None:
            return value
        return Decimal(value) / self.scale

    def to_python(self, value):
        """Convert input value to decimal, handling various input types.
        
        **Args:**
            value: Input value (int, str, or Decimal)
            
        **Returns:**
            Decimal value scaled by 1/scale
            
        **Raises:**
            ValueError: If value cannot be converted to Decimal
        """
        if value is None:
            return value
        if isinstance(value, Decimal):
            return value
        try:
            if isinstance(value, (int, str)):
                return Decimal(str(value)) / self.scale
            raise ValueError("Invalid value for FixedPointField")
        except (TypeError, ValueError, InvalidOperation):
            raise ValueError("Invalid value for FixedPointField")

    def get_prep_value(self, value):
        """Convert decimal value to integer for database storage.
        
        **Args:**
            value: Decimal value to store
            
        **Returns:**
            Integer value scaled by scale factor
        """
        if value is None:
            return value
        value = Decimal(str(value))  # Convert to Decimal to avoid float precision issues
        return int(value * self.scale) 