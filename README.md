# Phaser Game - 4X Space Empire

Turn-based 4X space empire game written using Phaser 3 with TypeScript.

## Documentation
- [Game Structure](docs/GameStructure.md) - Overview of game views and screens
- [Testing Guide](docs/TestingGuide.md) - Comprehensive guide to running and writing tests

## Project Structure
- **Game UI**: Phaser 3 with TypeScript
- **Backend**: FastAPI (Python) - Coming soon
- **Data Store**: To be determined - Coming soon

## Tech Stack
- Phaser 3 for game development
- TypeScript for type-safe JavaScript
- Webpack for bundling
- FastAPI for backend API (coming soon)
- Docker with docker-compose for development

## Prerequisites
- Node.js (v14+)
- npm (v6+)
- Docker and Docker Compose (for containerized development)

## Getting Started

### Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/phaser-game.git
cd phaser-game
```

2. Build and start the containers:
```bash
docker-compose up
```

3. Open your browser and navigate to `http://localhost:8080`

### Running Tests

The project includes a convenient test script (`test.sh`) that handles both frontend and backend tests. Always use this script rather than direct docker-compose commands to ensure proper test environment setup.

#### Frontend Tests

```bash
# Run basic frontend tests
./test.sh frontend

# Run frontend tests in watch mode
./test.sh frontend --watch

# Run frontend tests with coverage report
./test.sh frontend --coverage
```

#### Backend Tests

```bash
# Run basic backend tests
./test.sh backend

# Run backend tests with verbose output
./test.sh backend --verbose

# Run backend tests with coverage report
./test.sh backend --coverage
```

#### Running All Tests

```bash
# Run both frontend and backend tests
./test.sh all
```

### How Tests Work

1. The `test.sh` script uses `docker-compose.test.yml` to set up Docker containers for testing
2. For backend tests, it mounts the backend directory to `/app` in the container
3. Inside the container, it runs the `run_tests.sh` script which sets the Python path and runs pytest

### Important Rule

**ONLY use the `test.sh` script for running tests. DO NOT run tests directly with npm or pytest commands.**

This rule ensures consistency across development environments and simplifies the development workflow.

### Troubleshooting Tests

If you encounter import errors in backend tests:
1. Ensure all directories have proper `__init__.py` files
2. Check that the `PYTHONPATH` environment variable is correctly set in the Docker container
3. Verify you're using the `test.sh` script rather than running pytest directly

## Project Status
This project is in the early stages of development. Currently, only a basic skeleton with a blank screen is implemented.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
