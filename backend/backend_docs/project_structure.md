# Project Structure

## Overview
The backend is a Django application organized into several apps, each handling specific functionality for the 4X space conquest game.

## Directory Structure
```
backend/
├── Dockerfile              # Docker configuration for the backend service
├── requirements.txt        # Python package dependencies
├── manage.py              # Django management script
├── spacegame/            # Main Django project directory
│   ├── __init__.py
│   ├── asgi.py           # ASGI configuration
│   ├── settings.py       # Django settings
│   ├── urls.py           # URL routing configuration
│   └── wsgi.py           # WSGI configuration
├── core/                 # Core functionality and shared components
│   ├── __init__.py
│   ├── fields.py         # Custom model fields
│   ├── serializers.py    # Base serializer classes
│   ├── views.py         # Base view classes
│   └── tests/            # Core app tests
│       ├── __init__.py
│       └── test_fields.py
├── celestial/           # Celestial objects management
│   ├── __init__.py
│   ├── models.py        # Celestial models (Planet, Star, etc.)
│   ├── serializers.py   # API serializers
│   ├── views.py        # API views and viewsets
│   ├── urls.py         # URL routing
│   ├── migrations/      # Database migrations
│   └── tests/          # Celestial app tests
│       ├── __init__.py
│       ├── test_api.py
│       ├── test_config.py
│       └── test_models.py
├── empire/             # Empire and faction management
│   ├── __init__.py
│   ├── models.py       # Empire and faction models
│   └── tests/          # Empire app tests
├── research/           # Technology and research system
│   ├── __init__.py
│   ├── models.py       # Technology and research models
│   ├── serializers.py  # API serializers
│   ├── views.py       # API views and viewsets
│   ├── urls.py        # URL routing
│   ├── migrations/     # Database migrations
│   └── tests/         # Research app tests
│       ├── __init__.py
│       ├── test_api.py
│       └── test_models.py
├── units/              # Military and civilian units
│   ├── __init__.py
│   ├── models.py       # Unit models
│   └── tests/          # Unit tests
└── backend_docs/        # Backend documentation
    ├── api.md          # API documentation
    ├── models.md       # Model documentation
    ├── project_structure.md
    ├── revision_history.md
    └── current_task.md
```

## Key Components
- Django 5.0.2 as the web framework
- Django REST Framework for API development
- PostgreSQL for the database
- Docker for containerization
- JWT for authentication
- Redis for caching (planned)

## Development Environment
- Development server runs on port 8080
- Docker Compose manages the development environment
- Make commands available for common tasks:
  - `make backend` - Run the development server
  - `make backend-shell [command]` - Run a command in the backend container or open a shell
  - `make test-backend` - Run backend tests

## Apps

### Core
Located in `backend/core/`
- Provides shared functionality across apps
- Custom model fields:
  - `FixedPointField`: Precise decimal storage using integer scaling
- Base classes:
  - Base serializers for common patterns
  - Base viewsets with shared functionality
  - Common test utilities

### Celestial
Located in `backend/celestial/`
- Manages celestial entities in the game universe
- Models:
  - `Star`: Central star in a star system
    - Determines system characteristics
    - Affects resource generation
  - `Planet`: Represents planets with resource production
    - Resource production fields (mineral, organic, radioactive, exotic)
    - Resource storage capacity fields
    - Colony support capabilities
    - All resource values use FixedPointField for precise storage
  - `AsteroidBelt`: Resource-rich regions
    - Mining potential
    - Strategic value
- API endpoints:
  - GET /api/celestial/stars/ - List star systems
  - GET /api/celestial/planets/ - List planets
  - GET /api/celestial/asteroid-belts/ - List asteroid belts

### Empire
Located in `backend/empire/`
- Manages player empires and factions
- Models:
  - `Empire`: Player's civilization
    - Resource management
    - Planet and asteroid belt ownership
    - Technology research tracking
  - `Faction`: Sub-groups within empires
- Features:
  - Resource storage and management
  - Celestial body ownership
  - Integration with technology system

### Research
Located in `backend/research/`
- Manages technology and research system
- Models:
  - `Technology`: Available technologies
    - Name and description
    - Research cost
    - Prerequisites
    - Category (military, economic, scientific, diplomatic)
  - `EmpireTechnology`: Empire's research progress
    - Tracks research points
    - Links technology to empire
    - Enforces unique technology-empire pairs
- Features:
  - Technology tree with prerequisites
  - Research progress tracking
  - Category-based organization
  - Precise decimal storage for costs and progress

### Units (In Progress)
Located in `backend/units/`
- Military and civilian unit management
- Planned models:
  - `MilitaryUnit`: Combat units
  - `CivilianUnit`: Non-combat units
  - `Fleet`: Unit groupings 