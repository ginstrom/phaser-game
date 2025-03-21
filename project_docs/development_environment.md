# Development Environment Setup

This document describes the development environment for the Space Conquest Game project.

## Project Structure

```
phaser-game/
├── backend/           # Django backend application
│   ├── requirements.txt
│   └── backend_docs/  # Backend-specific documentation
├── frontend/         # Pixi.js frontend application
│   ├── package.json
│   └── .cursorrules  # Frontend development rules
├── docker/           # Docker configuration files
│   ├── Dockerfile
│   ├── docker-compose.yml     # Main docker-compose configuration
│   └── docker-compose.dev.yml # Development and testing configuration
├── project_docs/     # Project documentation
├── Makefile         # Build and development commands
└── .cursorrules     # Project-specific development rules
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
- `make backend` - Run the Django development server
- `make test` - Run all tests (backend and frontend)
- `make test-backend` - Run backend tests only
- `make test-frontend` - Run frontend tests (not implemented yet)

#### Backend Container

The backend container provides a development environment with:
- Python 3.11
- All required dependencies installed
- Volume-mounted backend directory for live code changes
- Non-root user for security

To start development:

1. Start the backend server:
   ```bash
   make backend
   ```

2. For development tasks, open a backend shell:
   ```bash
   make backend-shell
   ```

3. The shell will be in the `/app` directory where you can run Django commands:
   ```bash
   # Run migrations
   python manage.py migrate

   # Create a superuser
   python manage.py createsuperuser
   ```

### Testing

The project uses pytest for backend testing. To run tests:

```bash
# Run all tests
make test

# Run only backend tests
make test-backend
```

### Frontend Development

The frontend is a web-based client built with:
- Pixi.js for 2D game rendering
- TypeScript for type safety
- Webpack for bundling
- Jest for testing

#### Frontend Container

The frontend container provides:
- Node.js 20 environment
- NPM for package management
- Volume-mounted frontend directory for live code changes
- Hot module reloading for development

To start frontend development:

1. Start the frontend development server:
   ```bash
   make frontend
   ```

2. For frontend development tasks:
   ```bash
   make frontend-shell
   ```

## Docker Configuration

### Backend Dockerfile

The backend Dockerfile (`docker/Dockerfile`) provides:
- Python 3.11 slim base image
- System dependencies (build-essential, libpq-dev)
- Python dependencies from requirements.txt
- Non-root user for security
- Development server configuration

### Docker Compose Files

The project uses two docker-compose files:

1. `docker/docker-compose.yml` - Main configuration for development:
   - Backend service for running the Django server
   - Backend shell service for development
   - Volume mounting for live code changes

2. `docker/docker-compose.dev.yml` - Development and testing configuration:
   - Test environment setup
   - Additional development tools

## Next Steps

[x] Set up basic project structure
[x] Configure Docker development environment
[x] Set up Django backend
[] Implement API for celestial app
[] Create units app
[] Implement API for units app
[] Create empire app
[] Implement API for empire app
[] Create research app
[] Implement API for research app
[] Create API documentation
[] Create skeleton pixi.js front-end
[] Implement basic game rendering
[] Add turn-based game logic
[] Implement resource management
[] Add combat system