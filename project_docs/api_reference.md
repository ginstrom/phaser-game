# Space Conquest Game API Reference

See [backend/backend_docs/api.md](../backend/backend_docs/api.md) for the API reference.

## Star System Validation Rules

### Orbital Position Constraints
- Each orbit in a star system can only be occupied by one celestial body (planet or asteroid belt)
- Attempting to place a celestial body in an occupied orbit will result in a ValidationError
- Valid orbit numbers are positive integers from 1 to MAX_ORBITS (5)
- These constraints are enforced at both the model and API level

### API Endpoints Affected
- POST /api/systems/{id}/add_planet/
- POST /api/systems/{id}/add_asteroid_belt/
- PUT /api/planets/{id}/
- PUT /api/asteroid_belts/{id}/

### Error Responses
When attempting to place a celestial body in an occupied orbit:
```json
{
    "error": "Orbit X is already occupied by another celestial body in this system"
}
```