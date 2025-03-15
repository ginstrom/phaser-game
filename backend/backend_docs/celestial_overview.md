# Celestial App Overview

The Celestial app is a core component of the 4X space conquest game, responsible for managing celestial bodies and their resources in the game world.

## Components

### Models
- `Star`: Represents stars with different types (blue, white, yellow, orange, brown)
- `Planet`: Represents planets with resource production and storage capabilities
- `AsteroidBelt`: Represents asteroid belts with resource production capabilities

### API Endpoints
The app provides REST API endpoints for managing all celestial bodies. See `celestial_views.md` for detailed endpoint documentation.

### Data Serialization
Handles data transformation between JSON and model instances. See `celestial_serializers.md` for detailed serializer documentation.

## Resource System

### Production
All celestial bodies (except stars) have resource production capabilities for:
- Minerals
- Organic materials
- Radioactive materials
- Exotic materials

Base production values default to 50 units per turn.

### Storage
Planets have storage capacity for all resource types, defaulting to 100 units per resource type.
Asteroid belts do not have storage capacity - they only produce resources.

## Usage

### Creating New Celestial Bodies
```python
# Create a star
from celestial.models import Star
blue_star = Star.objects.create(star_type='blue')

# Create a planet
from celestial.models import Planet
planet = Planet.objects.create(
    mineral_production=75,
    organic_production=50,
    radioactive_production=25,
    exotic_production=60
)

# Create an asteroid belt
from celestial.models import AsteroidBelt
belt = AsteroidBelt.objects.create(
    mineral_production=100,
    organic_production=30,
    radioactive_production=45,
    exotic_production=20
)
```

### API Interaction
```bash
# List all planets
curl -X GET http://localhost:8000/api/planets/

# Create a new star
curl -X POST http://localhost:8000/api/stars/ \
    -H "Content-Type: application/json" \
    -d '{"star_type": "yellow"}'

# Update a planet's resource production
curl -X PATCH http://localhost:8000/api/planets/1/ \
    -H "Content-Type: application/json" \
    -d '{"mineral_production": 75}'
```

## Related Documentation
- [Models Documentation](models.md)
- [Views Documentation](celestial_views.md)
- [Serializers Documentation](celestial_serializers.md) 