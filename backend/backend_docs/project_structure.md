# Project Structure

## Overview
The backend is a Django application organized into several apps, each handling specific functionality.

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
│   └── tests/            # Core app tests
│       ├── __init__.py
│       └── test_fields.py
├── celestial/           # Celestial objects management
│   ├── __init__.py
│   ├── models.py        # Celestial models (Planet, etc.)
│   ├── migrations/      # Database migrations
│   └── tests/          # Celestial app tests
│       ├── __init__.py
│       ├── test_config.py
│       └── test_models.py
└── backend_docs/        # Backend documentation
    ├── project_structure.md
    ├── revision_history.md
    └── current_task.md
```

## Key Components
- Django 5.0.2 as the web framework
- Django REST Framework for API development
- PostgreSQL (planned) for the database
- Docker for containerization

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

### Celestial
Located in `backend/celestial/`
- Manages celestial entities like planets
- Models:
  - `Planet`: Represents planets with resource production and storage
    - Resource production fields (mineral, organic, radioactive, exotic)
    - Resource storage capacity fields
    - All resource values use FixedPointField for precise storage
- Tests organized in dedicated test directory
  - Configuration tests
  - Model tests with comprehensive coverage 