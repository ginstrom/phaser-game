# Revision History

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