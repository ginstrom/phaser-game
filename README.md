# Phaser Game - 4X Space Empire

Turn-based 4X space empire game written using Phaser 3 with TypeScript.

## Documentation
- [Game Structure](docs/GameStructure.md) - Overview of game views and screens

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

Run the tests using docker-compose:
```bash
docker-compose -f docker-compose.test.yml run frontend
```

Run tests in watch mode:
```bash
docker-compose -f docker-compose.test.yml run frontend-watch
```

Run tests with coverage:
```bash
docker-compose -f docker-compose.test.yml run frontend-coverage
```

### Important Rule

**ONLY use docker-compose for running the game or tests. DO NOT run the game code or tests directly in the console.**

This rule ensures consistency across development environments and simplifies the development workflow.

## Project Status
This project is in the early stages of development. Currently, only a basic skeleton with a blank screen is implemented.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
