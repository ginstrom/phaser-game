# Space Empire 4X Game Backend

This is the backend service for the Space Empire 4X game, providing API endpoints for game state management, player interactions, and game logic processing.

## Tech Stack

- **Framework**: FastAPI (Python 3.9+)
- **Database**: PostgreSQL (coming soon)
- **Authentication**: JWT-based authentication
- **API Documentation**: OpenAPI (Swagger UI)
- **Testing**: pytest
- **Container**: Docker

## High-Level Design

### Architecture Overview

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Game Client   │ ←── │  FastAPI Server │ ←── │    Database     │
│   (Phaser.js)   │     │   (Backend)     │     │  (PostgreSQL)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Core Components

1. **Game State Manager**
   - Handles game session state
   - Manages turn processing
   - Coordinates player actions

2. **Empire Manager**
   - Colony management
   - Resource tracking
   - Technology research

3. **Combat System**
   - Fleet movement
   - Battle resolution
   - Combat calculations

4. **Map Generator**
   - Procedural galaxy generation
   - Star system placement
   - Resource distribution

## API Structure

The API follows RESTful principles with the following main endpoints:

- `/api/v1/games` - Game session management
- `/api/v1/empires` - Empire and colony operations
- `/api/v1/research` - Technology research
- `/api/v1/combat` - Combat operations
- `/api/v1/maps` - Map generation and retrieval

## Development Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. Run development server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Testing

Always use the root project's `test.sh` script for running tests:

```bash
./test.sh backend
```

## API Documentation

When running locally, access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Contributing

1. Follow PEP 8 style guide
2. Write tests for new features
3. Update API documentation
4. Use type hints
5. Follow Git commit message conventions 