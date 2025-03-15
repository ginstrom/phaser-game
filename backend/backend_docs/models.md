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

##### Orbital Position
- `orbit`: The orbital position from the star (1 being closest), must be a positive integer

#### Usage Example
```python
from celestial.models import Planet

# Create a planet with default values (production=50, storage=100, orbit=1)
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
    exotic_storage_capacity=125.75,
    orbit=3
)
```

#### Implementation Details
- All resource values are stored using `FixedPointField` which maintains precise decimal values without floating-point errors
- Values are stored internally as integers with a scale factor of 1000 (e.g., 50.5 is stored as 50500)
- The model provides string representation in the format "Planet {id}"
- Orbit must be a positive integer (validated before saving)

#### Testing
The model includes comprehensive test coverage:
- Default value initialization
- Custom value creation and retrieval
- Decimal precision maintenance
- String representation
- Orbit validation

### AsteroidBelt
Represents an asteroid belt in the game world with resource production capabilities.

#### Fields

##### Resource Production
All production fields use `FixedPointField` for precise decimal storage. Default value is 50.

- `mineral_production`: Base mineral production per turn
- `organic_production`: Base organic production per turn
- `radioactive_production`: Base radioactive production per turn
- `exotic_production`: Base exotic production per turn

##### Orbital Position
- `orbit`: The orbital position from the star (1 being closest), must be a positive integer

#### Usage Example
```python
from celestial.models import AsteroidBelt

# Create an asteroid belt with default values (production=50, orbit=1)
default_belt = AsteroidBelt.objects.create()

# Create an asteroid belt with custom values
custom_belt = AsteroidBelt.objects.create(
    mineral_production=75.5,
    organic_production=25.25,
    radioactive_production=60.75,
    exotic_production=40.25,
    orbit=4
)
```

#### Implementation Details
- All resource values are stored using `FixedPointField` which maintains precise decimal values without floating-point errors
- Values are stored internally as integers with a scale factor of 1000 (e.g., 50.5 is stored as 50500)
- Unlike planets, asteroid belts do not have storage capacity
- The model provides string representation in the format "Asteroid Belt {id}"
- Orbit must be a positive integer (validated before saving)

#### Testing
The model includes comprehensive test coverage:
- Default value initialization
- Custom value creation and retrieval
- Decimal precision maintenance
- String representation
- Orbit validation 

## System

A star system in the galaxy. Each system has a unique position in the galaxy grid and contains exactly one star. The system can have up to MAX_ORBITS (5) planets and/or asteroid belts, with each orbit being occupied by at most one celestial body.

### Fields

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| x | integer | X coordinate in the galaxy | Required |
| y | integer | Y coordinate in the galaxy | Required |
| star | OneToOneField | The star at the center of this system | Required |

### Relationships

- `star`: One-to-one relationship with Star model
- `planets`: One-to-many relationship with Planet model
- `asteroid_belts`: One-to-many relationship with AsteroidBelt model

### Constraints

- The combination of x and y coordinates must be unique (no two systems can occupy the same position)
- Each system must have exactly one star
- The total number of planets and asteroid belts cannot exceed MAX_ORBITS (5)
- Each orbit (1 to MAX_ORBITS) can be occupied by either a planet or an asteroid belt, but not both

### Methods

- `clean()`: Validates the system constraints regarding orbit usage
- `save()`: Ensures the system constraints are validated before and after saving

### Example Usage

```python
# Create a new system
star = Star.objects.create(star_type='yellow')
system = System.objects.create(x=1, y=1, star=star)

# Add a planet to orbit 1
planet = Planet.objects.create(system=system, orbit=1)

# Add an asteroid belt to orbit 2
belt = AsteroidBelt.objects.create(system=system, orbit=2)

# This will raise ValidationError (duplicate orbit)
planet2 = Planet.objects.create(system=system, orbit=2)  # Error!

# This will raise ValidationError (exceeds MAX_ORBITS)
for i in range(1, 7):
    Planet.objects.create(system=system, orbit=i)  # Error on 6th planet! 