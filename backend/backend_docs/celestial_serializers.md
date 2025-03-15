# Celestial Serializers Documentation

This document describes the serializers used for data transformation in the celestial app.

## Serializers

### PlanetSerializer

Handles serialization and deserialization of Planet model instances.

#### Fields

All decimal fields use max_digits=10 and decimal_places=2.

- `id` (integer): Planet identifier
- `mineral_production` (decimal): Base mineral production per turn
- `organic_production` (decimal): Base organic production per turn
- `radioactive_production` (decimal): Base radioactive production per turn
- `exotic_production` (decimal): Base exotic production per turn
- `mineral_storage_capacity` (decimal): Maximum mineral storage capacity
- `organic_storage_capacity` (decimal): Maximum organic storage capacity
- `radioactive_storage_capacity` (decimal): Maximum radioactive storage capacity
- `exotic_storage_capacity` (decimal): Maximum exotic storage capacity

### StarSerializer

Handles serialization and deserialization of Star model instances.

#### Fields

- `id` (integer): Star identifier
- `star_type` (string): Type of star (choices: blue, white, yellow, orange, brown)

### AsteroidBeltSerializer

Handles serialization and deserialization of AsteroidBelt model instances.

#### Fields

All decimal fields use max_digits=10 and decimal_places=2.

- `id` (integer): Asteroid belt identifier
- `mineral_production` (decimal): Base mineral production per turn
- `organic_production` (decimal): Base organic production per turn
- `radioactive_production` (decimal): Base radioactive production per turn
- `exotic_production` (decimal): Base exotic production per turn 