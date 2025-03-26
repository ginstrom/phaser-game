# Revision History

## 2025-03-26: Refactor FixedPointField Tests
### Changes
- Removed test-only TestModel and associated migrations
- Updated FixedPointField tests to use Planet model
- Cleaned up core app migrations
- All tests passing with real model usage

### Implementation Details
- Removed redundant test model and migrations
- Improved test maintainability by using actual production model
- Verified correct decimal scale handling
- Maintained full test coverage of FixedPointField functionality

## 2025-03-25: Added Technology and EmpireTechnology Models

### Changes
- Added Technology model with fields:
  - name (unique)
  - description
  - cost (FixedPointField)
  - prerequisites (self-referential many-to-many)
  - category (enum: military, economic, scientific, diplomatic)
- Added EmpireTechnology model with:
  - Foreign keys to Technology and Empire
  - research_points tracking
  - Unique constraint on technology-empire pairs
  - is_complete property
- Added comprehensive test coverage for both models
- All tests passing

### Implementation Details
- Used FixedPointField for precise decimal storage
- Implemented proper transaction handling in tests
- Added test cleanup code to handle database state
- Added proper validation for unique constraints
- Updated documentation with model details

## 2025-03-21: Add Timestamp Fields to Game Model
- Added `created` and `modified` timestamp fields to Game model
- All timestamps are stored in UTC
- Added comprehensive tests for timestamp functionality
- Reset migrations to clean state

## 2025-03-15: Empire Model Implementation
- Added Empire model with relationships to Player and Race models
- Added support for managing planets and asteroid belts
- Implemented resource storage and capacity tracking
- Added API endpoints for Empire CRUD operations
- Added comprehensive tests for model and API
- Updated documentation 

## 2024-03-21: Game Model and System Coordinates
- Fixed Game model validation and improved System coordinate uniqueness handling
- Added proper transaction handling in tests and fixed empire-game relationship tests

## 2024-03-21: Game Model Added
- Added Game model to track game state and turns
- Implemented game-scoped uniqueness for system coordinates

## 2024-03-16: GalaxySize Enum Implementation
- Converted GalaxySize to proper Python Enum with system_count property
- Updated serializer and tests to work with enum implementation

## 2024-03-15: System Model and API
- Added System model with unique coordinates and celestial body relationships
- Added CRUD operations and orbit management endpoints

## 2024-03-15: Race Model and API
- Added Race model with unique name field and CRUD operations
- Added comprehensive test coverage and documentation

## 2024-03-15: Celestial Models
- Added Star, Planet, and AsteroidBelt models with resource mechanics
- Implemented orbit field and resource production/storage systems

## 2024-03-14: Initial Setup
- Created Django project structure with docker configuration
- Set up PostgreSQL database and test environment
- Added initial requirements and Makefile commands

## Previous Changes
// ... existing code ... 