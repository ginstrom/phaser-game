# Admin Interface Documentation

## Celestial Bodies Management

### Orbit Management
- Each star system can have up to 5 orbital positions
- Each orbit can only be occupied by one celestial body (planet or asteroid belt)
- Orbits are numbered 1-5, with 1 being closest to the star
- The system enforces orbit uniqueness at multiple levels:
  - Model level: Prevents saving invalid orbit configurations
  - Form level: Prevents selecting already occupied orbits
  - System level: Validates total number of orbits and orbit uniqueness

### Adding Celestial Bodies
1. Navigate to the System detail page
2. Click "Add another Planet" or "Add another Asteroid Belt"
3. Select an available orbit from the dropdown
4. Fill in other required fields
5. Click Save

### Orbit Selection
- The orbit dropdown only shows available orbits
- If all orbits are taken, the field will be disabled with a message
- When editing an existing celestial body, its current orbit is excluded from the used orbits list

### Validation Rules
1. No two celestial bodies can share the same orbit
2. Total number of orbits cannot exceed System.MAX_ORBITS (5)
3. Orbits must be positive integers
4. Each orbit can only be occupied by one type of celestial body (planet or asteroid belt)

### Error Handling
- Clear error messages indicate when:
  - An orbit is already occupied
  - The maximum number of orbits is reached
  - Invalid orbit numbers are selected 