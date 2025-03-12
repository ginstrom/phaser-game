# Space Empire 4X Game

A turn-based 4X (eXplore, eXpand, eXploit, eXterminate) space strategy game built with Phaser 3, FastAPI, and PostgreSQL.

## Quick Start

1. **Prerequisites**
   - Docker and Docker Compose
   - Node.js 16+ (for local development)
   - Python 3.9+ (for local development)

2. **Run the Game**
   ```bash
   # Start all services
   docker-compose up

   # Frontend: http://localhost:3000
   # API docs: http://localhost:8000/docs
   ```

## Development

```bash
# Start frontend only
docker-compose up frontend

# Start backend only
docker-compose up backend

# Start database only
docker-compose up db
```

## Testing

```bash
# Run all tests
./test.sh all

# Run frontend tests
./test.sh frontend

# Run backend tests
./test.sh backend

# Run with coverage
./test.sh frontend --coverage
./test.sh backend --coverage
```

## Project Structure

```
.
├── frontend/     # Phaser.js game client
├── backend/      # FastAPI server
├── config/       # Shared configuration
├── docs/         # Documentation
└── docker/       # Docker configuration
```

## Documentation

- [Game Architecture](docs/GameStructure.md)
- [Testing Guide](docs/TestingGuide.md)

## Tech Stack

- **Frontend**: Phaser 3, TypeScript, Webpack
- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **DevOps**: Docker, Docker Compose

## License

MIT
