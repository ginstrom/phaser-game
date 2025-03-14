# Project Structure

## Overview
The backend is a Django-based REST API server that manages the game state and business logic for the space conquest game.

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
└── backend_docs/         # Backend documentation
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
  - `make backend-shell` - Open a shell in the backend container 