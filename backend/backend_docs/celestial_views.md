# Celestial Views Documentation

This document describes the API endpoints available in the celestial app.

## ViewSets

### PlanetViewSet

REST API endpoint for managing planets in the game world.

#### Endpoints

- `GET /api/planets/` - List all planets
- `POST /api/planets/` - Create a new planet
- `GET /api/planets/{id}/` - Retrieve a specific planet
- `PUT /api/planets/{id}/` - Update a specific planet
- `PATCH /api/planets/{id}/` - Partially update a specific planet
- `DELETE /api/planets/{id}/` - Delete a specific planet

### StarViewSet

REST API endpoint for managing stars in the game world.

#### Endpoints

- `GET /api/stars/` - List all stars
- `POST /api/stars/` - Create a new star
- `GET /api/stars/{id}/` - Retrieve a specific star
- `PUT /api/stars/{id}/` - Update a specific star
- `PATCH /api/stars/{id}/` - Partially update a specific star
- `DELETE /api/stars/{id}/` - Delete a specific star

### AsteroidBeltViewSet

REST API endpoint for managing asteroid belts in the game world.

#### Endpoints

- `GET /api/asteroid-belts/` - List all asteroid belts
- `POST /api/asteroid-belts/` - Create a new asteroid belt
- `GET /api/asteroid-belts/{id}/` - Retrieve a specific asteroid belt
- `PUT /api/asteroid-belts/{id}/` - Update a specific asteroid belt
- `PATCH /api/asteroid-belts/{id}/` - Partially update a specific asteroid belt
- `DELETE /api/asteroid-belts/{id}/` - Delete a specific asteroid belt 