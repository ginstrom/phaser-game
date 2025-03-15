# Models Documentation

## Celestial Models

### Star
Represents a star in the game world with its type classification.

#### Fields

##### Star Type
- `star_type`: The type of star (choices: blue, white, yellow, orange, brown)

#### Usage Example
```python
from celestial.models import Star

# Create a blue star
blue_star = Star.objects.create(star_type='blue')

# Create a yellow star
yellow_star = Star.objects.create(star_type='yellow')
```

#### Implementation Details
- Star type is stored as a CharField with choices
- The model provides string representation in the format "[Type] Star [id]" (e.g., "Blue Star 1")

#### Testing
The model includes test coverage for:
- Star creation with valid types
- Validation of invalid star types
- String representation
- Available star type choices

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

### AsteroidBelt
Represents an asteroid belt in the game world with resource production capabilities.

#### Fields

##### Resource Production
All production fields use `FixedPointField` for precise decimal storage. Default value is 50.

- `mineral_production`: Base mineral production per turn
- `organic_production`: Base organic production per turn
- `radioactive_production`: Base radioactive production per turn
- `exotic_production`: Base exotic production per turn

#### Usage Example
```python
from celestial.models import AsteroidBelt

# Create an asteroid belt with default values (production=50)
default_belt = AsteroidBelt.objects.create()

# Create an asteroid belt with custom values
custom_belt = AsteroidBelt.objects.create(
    mineral_production=75.5,
    organic_production=25.25,
    radioactive_production=60.75,
    exotic_production=40.25
)
```

#### Implementation Details
- All resource values are stored using `FixedPointField` which maintains precise decimal values without floating-point errors
- Values are stored internally as integers with a scale factor of 1000 (e.g., 50.5 is stored as 50500)
- Unlike planets, asteroid belts do not have storage capacity
- The model provides string representation in the format "Asteroid Belt {id}"

#### Testing
The model includes comprehensive test coverage:
- Default value initialization
- Custom value creation and retrieval
- Decimal precision maintenance
- String representation 