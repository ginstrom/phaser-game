# Models Documentation

## Celestial Models

### Planet
Represents a planet in the game world with resource production and storage capabilities.

#### Fields

##### Resource Production
All production fields use `FixedPointField` for precise decimal storage. Default value is 50.

- `mineral_production`: Base mineral production per turn
- `organic_production`: Base organic production per turn
- `radioactive_production`: Base radioactive production per turn
- `exotic_production`: Base exotic production per turn

##### Resource Storage Capacity
All storage capacity fields use `FixedPointField`. Default value is 100.

- `mineral_storage_capacity`: Maximum mineral storage capacity
- `organic_storage_capacity`: Maximum organic storage capacity
- `radioactive_storage_capacity`: Maximum radioactive storage capacity
- `exotic_storage_capacity`: Maximum exotic storage capacity

#### Usage Example
```python
from celestial.models import Planet

# Create a planet with default values (production=50, storage=100)
default_planet = Planet.objects.create()

# Create a planet with custom values
custom_planet = Planet.objects.create(
    mineral_production=75.5,
    organic_production=25.25,
    radioactive_production=60.75,
    exotic_production=40.25,
    mineral_storage_capacity=150.5,
    organic_storage_capacity=200.75,
    radioactive_storage_capacity=175.25,
    exotic_storage_capacity=125.75
)
```

#### Implementation Details
- All resource values are stored using `FixedPointField` which maintains precise decimal values without floating-point errors
- Values are stored internally as integers with a scale factor of 1000 (e.g., 50.5 is stored as 50500)
- The model provides string representation in the format "Planet {id}"

#### Testing
The model includes comprehensive test coverage:
- Default value initialization
- Custom value creation and retrieval
- Decimal precision maintenance
- String representation 