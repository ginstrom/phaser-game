# Development Environment Setup

This document describes the development environment for the Space Conquest Game project.

## Project Structure

```
phaser-game/
├── backend/           # Django backend application
│   └── requirements.txt
├── docker/           # Docker configuration files
│   ├── Dockerfile
│   └── docker-compose.dev.yml
├── frontend/         # Frontend application (to be added)
└── Makefile         # Build and development commands
```

## Prerequisites

- Docker and Docker Compose
- Make

## Development Environment

The project uses Docker for development to ensure consistent environments across all developers. The backend is built with Django and uses PostgreSQL as the database.

### Backend Development

The backend is a Django application with the following key components:

- Django 5.0.2
- Django REST Framework
- PostgreSQL database
- Development tools (black, flake8, pytest)

#### Available Make Commands

- `make help` - Display available make commands
- `make backend-shell` - Open an interactive shell in the backend container

#### Backend Container

The backend container provides a development environment with:
- Python 3.11
- All required dependencies installed
- Volume-mounted backend directory for live code changes
- Non-root user for security

To start development:

1. Open a backend shell:
   ```bash
   make backend-shell
   ```

2. The shell will be in the `/app` directory where you can run Django commands:
   ```bash
   # Create a new Django project
   django-admin startproject backend .

   # Run migrations
   python manage.py migrate

   # Start the development server
   python manage.py runserver 0.0.0.0:8000
   ```

### Frontend Development

Frontend development setup will be added in a future update.

## Docker Configuration

### Backend Dockerfile

The backend Dockerfile (`docker/Dockerfile`) provides:
- Python 3.11 slim base image
- System dependencies (build-essential, libpq-dev)
- Python dependencies from requirements.txt
- Non-root user for security
- Development server configuration

### Development Docker Compose

The development docker-compose file (`docker/docker-compose.dev.yml`) provides:
- Backend shell service for development
- Volume mounting for live code changes
- Interactive shell access

## Next Steps

1. Set up the Django project structure
2. Configure database settings
3. Set up frontend development environment
4. Add testing infrastructure 