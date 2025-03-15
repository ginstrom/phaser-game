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
```

## Player Model

### Overview
The Player model represents a player in the game, which can be either a human player or a computer-controlled player.

### Fields
- `id` (AutoField): Primary key
- `player_type` (CharField): Type of player
  - Choices: "human" or "computer"
  - Default: "human"
  - Max length: 10 characters

### Usage Example
```python
from play.models import Player

# Create a human player (default)
human_player = Player.objects.create()

# Create a computer player
computer_player = Player.objects.create(player_type=Player.PlayerType.COMPUTER)

# Query players by type
human_players = Player.objects.filter(player_type=Player.PlayerType.HUMAN)
computer_players = Player.objects.filter(player_type=Player.PlayerType.COMPUTER)
```

### Implementation Details
- Uses Django's TextChoices for player type enumeration
- Implements string representation for admin interface and debugging
- Includes app_label meta for proper app organization 

## Race

The Race model represents different playable races in the game.

### Fields

- `id` (AutoField): Primary key
- `name` (CharField): Unique name of the race
  - max_length: 100
  - unique: True

### Usage Example

```python
# Create a new race
race = Race.objects.create(name="Humans")

# Get all races
all_races = Race.objects.all()

# Get a specific race
human_race = Race.objects.get(name="Humans")

# Update a race
human_race.name = "Updated Race Name"
human_race.save()

# Delete a race
human_race.delete()
```

### Implementation Details

The Race model enforces unique names through a database constraint. This ensures that no two races can have the same name. The model provides a string representation that returns the race name for easy identification in admin interfaces and debugging. 

## Empire

The Empire model represents a player's empire in the game, including its race, controlled planets and asteroid belts, and resource storage.

### Fields

#### Basic Information
- `id` (AutoField): Primary key
- `name` (CharField): Name of the empire
  - max_length: 100
- `player` (ForeignKey): Reference to the Player who owns this empire
  - on_delete: CASCADE
  - related_name: 'empires'
- `race` (ForeignKey): Reference to the Race of this empire
  - on_delete: PROTECT
  - related_name: 'empires'

#### Celestial Body Relationships
- `planets` (ManyToManyField): Planets controlled by this empire
  - related_name: 'empire'
  - blank: True
- `asteroid_belts` (ManyToManyField): Asteroid belts controlled by this empire
  - related_name: 'empire'
  - blank: True

#### Resource Storage
- `mineral_storage` (IntegerField): Current mineral storage
  - default: 0
- `organic_storage` (IntegerField): Current organic storage
  - default: 0
- `radioactive_storage` (IntegerField): Current radioactive storage
  - default: 0
- `exotic_storage` (IntegerField): Current exotic storage
  - default: 0

### Properties

The Empire model provides several properties that calculate the total resource capacities from all controlled planets:

- `mineral_capacity`: Total mineral storage capacity from all planets
- `organic_capacity`: Total organic storage capacity from all planets
- `radioactive_capacity`: Total radioactive storage capacity from all planets
- `exotic_capacity`: Total exotic storage capacity from all planets

### Usage Example

```python
from play.models import Empire, Player, Race
from celestial.models import Planet, AsteroidBelt

# Create prerequisites
player = Player.objects.create(player_type=Player.PlayerType.HUMAN)
race = Race.objects.create(name="Test Race")

# Create an empire
empire = Empire.objects.create(
    name="Test Empire",
    player=player,
    race=race
)

# Add planets and asteroid belts
planet1 = Planet.objects.get(id=1)
planet2 = Planet.objects.get(id=2)
asteroid_belt = AsteroidBelt.objects.get(id=1)

empire.planets.add(planet1, planet2)
empire.asteroid_belts.add(asteroid_belt)

# Update resource storage
empire.mineral_storage = 100
empire.organic_storage = 200
empire.save()

# Get resource capacities
print(f"Mineral Capacity: {empire.mineral_capacity}")
print(f"Organic Capacity: {empire.organic_capacity}")
print(f"Radioactive Capacity: {empire.radioactive_capacity}")
print(f"Exotic Capacity: {empire.exotic_capacity}")
```

### Implementation Details
- Uses Django's ManyToManyField for flexible relationships with planets and asteroid belts
- Implements property methods to calculate total resource capacities
- Provides string representation in the format "Empire Name (Race Name)"
- Includes app_label meta for proper app organization

### Testing
The model includes comprehensive test coverage for:
- Empire creation with basic attributes
- Relationships with planets and asteroid belts
- Resource storage management
- Resource capacity calculations
- String representation

# ... existing code ... 