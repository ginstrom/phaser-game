# Revision History

## 2024-03-21: Fixed API Serialization Issues

### Changes
- Fixed SystemSerializer to properly handle star data during creation and updates
- Updated EmpireSerializer to correctly handle planet and asteroid belt assignments
- Fixed test cases to use correct field names (planet_ids, asteroid_belt_ids)
- All tests now passing (109 tests)

### Implementation Details
- Removed read_only=True from star field in SystemSerializer to allow creation/updates
- Updated empire update tests to use correct field names for related objects
- Fixed assertion checks in empire tests to handle nested serialization

## 2024-03-21 - Enhanced Star System Creation
- Added automatic celestial body creation to star systems
  - Added terran planet in orbit 1 with balanced resource production
  - Added asteroid belt in orbit 2 with mineral-rich production
  - Updated tests to verify celestial body creation
  - Improved system initialization with more realistic starting conditions
  - Updated documentation to reflect changes

## 2024-03-21 - Refactored Star System Creation
- Extracted star system creation logic into separate function
  - Created create_star_system function for single system creation
  - Updated create_star_systems to use new function
  - Added comprehensive test coverage for new function
  - Improved code modularity and reusability
  - Updated documentation to reflect changes

## 2024-03-15 - Added Orbit Field to Celestial Bodies
- Added orbit field to Planet and AsteroidBelt models
  - Implemented positive integer validation
  - Updated API endpoints to handle orbit field
  - Added comprehensive test coverage for orbit field
  - Updated documentation with orbit field details
  - Added test cleanup code to all test classes

## 2024-03-15 - AsteroidBelt Model Implementation
- Added AsteroidBelt model for resource production
  - Implemented production fields for mineral, organic, radioactive, and exotic resources
  - Used FixedPointField for precise decimal storage
  - Created REST API endpoints for AsteroidBelt management
  - Added model and API tests with comprehensive coverage
  - Updated documentation with AsteroidBelt model and API details

## 2024-03-15 - Star Model Implementation
- Added Star model with star type classification
  - Implemented star types: blue, white, yellow, orange, brown
  - Added model tests with comprehensive coverage
  - Created REST API endpoints for Star management
  - Added API tests for all CRUD operations
  - Updated documentation with Star model and API details

## 2024-03-15 - Planet Model and Test Organization
- Added Planet model with resource mechanics
  - Production fields for mineral, organic, radioactive, and exotic resources
  - Storage capacity fields for each resource type
  - Used FixedPointField for precise decimal storage
- Reorganized tests into dedicated test directories
  - Moved tests from test.py to tests/ directory
  - Split into test_config.py and test_models.py
  - Added comprehensive test coverage for Planet model
- Enhanced Makefile
  - Modified backend-shell to accept direct command arguments
  - Improved command passing for development tasks

## 2024-03-14 - Test Configuration Setup
- Added test settings with in-memory SQLite database
- Created docker-compose.dev.yml for development and testing
- Added test commands to Makefile
- Configured test environment with optimized settings

## 2024-03-14 - PostgreSQL Database Setup
- Added PostgreSQL service to docker-compose.yml
- Updated Django settings to use PostgreSQL
- Created and applied initial migrations
- Fixed port conflict by using port 5433 for PostgreSQL

## 2024-03-14 - Initial Backend Setup
- Created Django project structure with docker configuration
- Set up docker-compose with backend and backend-shell services
- Added Makefile commands for running the backend
- Configured ALLOWED_HOSTS for development
- Added initial requirements.txt with core dependencies

### Bug Fixes
- Fixed DisallowedHost error by adding appropriate hosts to ALLOWED_HOSTS in settings.py
- Fixed PostgreSQL port conflict by using port 5433

### Environment Setup
- Django 5.0.2
- Python 3.11
- PostgreSQL 16
- Development server running on port 8080
- Test environment using in-memory SQLite

## March 14, 2025
- Added celestial app for managing celestial entities (stars, planets)
- Improved docker-compose configuration with database health checks
  - Added healthcheck for PostgreSQL database
  - Modified backend services to wait for database health
  - Fixed startup sequence issues

## 2024-03-15
- Added System model with:
  - Unique x,y coordinates in galaxy
  - One-to-one relationship with Star
  - One-to-many relationships with Planet and AsteroidBelt
  - MAX_ORBITS (5) constraint for total celestial bodies
  - Validation for unique orbit usage
- Added System API endpoints:
  - CRUD operations for systems
  - Add planet to system
  - Add asteroid belt to system
- Added comprehensive tests for System model and API
- Updated documentation for System model and API endpoints

## [2024-03-15] Added Race Model and API
- Added Race model with unique name field
- Implemented Race API endpoints (CRUD operations)
- Added comprehensive test coverage for model and API
- Updated documentation for Race model and API endpoints
- Features:
  - Unique race names
  - Full CRUD operations via REST API
  - Validation for duplicate names

## 2025-03-15

### Empire Model Implementation
- Added Empire model with relationships to Player and Race models
- Added support for managing planets and asteroid belts
- Implemented resource storage and capacity tracking
- Added API endpoints for Empire CRUD operations
- Added comprehensive tests for model and API
- Updated documentation 

## Latest Changes

### Game Model and System Coordinates (2024-03-21)
- Fixed Game model validation to only run when explicitly called
- Improved System coordinate uniqueness handling
  - Added proper validation in SystemSerializer
  - Fixed coordinate uniqueness checks within game context
  - Added comprehensive test coverage for coordinate validation
- Fixed test suite issues
  - Added proper transaction handling in tests
  - Improved test cleanup and data isolation
  - Fixed empire-game relationship tests
- Updated documentation to reflect changes

### Game Model Added (2024-03-21)
- Added Game model to track game state and turns
- Added relationships from Empire and System to Game
- Implemented game-scoped uniqueness for system coordinates
- Added API endpoints for game management
- Added comprehensive tests for model and API
- Updated documentation 

## March 16, 2024

### GalaxySize Enum Implementation
- Converted GalaxySize to proper Python Enum
- Added system_count property and choices() method
- Updated serializer to use enum values
- Improved validation and error handling
- Updated tests to work with enum implementation

Benefits:
- Type safety through enum validation
- Better API documentation with DRF Spectacular
- Cleaner code with encapsulated system count logic
- More maintainable galaxy size handling 