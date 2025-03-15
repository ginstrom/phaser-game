from django.db import models
from decimal import Decimal, InvalidOperation


class FixedPointField(models.IntegerField):
    """
    A field that stores decimal numbers as integers with a scale factor to avoid floating point errors.
    For example, with scale=1000, the value 1.234 would be stored as 1234 in the database.
    """
    description = "Fixed-point decimal number stored as an integer"

    def __init__(self, scale=1000, *args, **kwargs):
        self.scale = scale
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.scale != 1000:
            kwargs['scale'] = self.scale
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return Decimal(value) / self.scale

    def to_python(self, value):
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
        if value is None:
            return value
        value = Decimal(str(value))  # Convert to Decimal to avoid float precision issues
        return int(value * self.scale) 