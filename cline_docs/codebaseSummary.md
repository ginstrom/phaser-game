# Codebase Summary

## Project Structure
```
phaser-game/
├── src/
│   ├── assets/         # Game assets (images, audio, etc.)
│   ├── scenes/         # Phaser scene files
│   │   ├── MainScene.ts       # Main game scene
│   │   ├── StartupScene.ts    # Main menu scene
│   │   ├── GalaxyScene.ts     # Galaxy view scene
│   │   ├── SystemScene.ts     # System view scene
│   │   └── PlanetScene.ts     # Planet view scene
│   ├── ui/             # UI components
│   │   ├── Button.ts          # Reusable button component
│   │   ├── Panel.ts           # Reusable panel component
│   │   └── TextStyles.ts      # Text style definitions
│   ├── objects/        # Game object classes
│   ├── utils/          # Utility functions
│   ├── __tests__/      # Test files
│   │   ├── index.test.ts      # Game initialization tests
│   │   ├── scenes/            # Scene tests
│   │   └── ui/                # UI component tests
│   └── index.ts        # Main entry point for the game
├── public/
│   └── index.html      # HTML entry point
├── backend/
│   ├── app/            # FastAPI application
│   │   ├── main.py     # Main application entry point
│   │   └── routers/    # API route handlers
│   │       ├── new_game.py    # New game endpoint
│   │       ├── load_game.py   # Load game endpoint
│   │       ├── settings.py    # Settings endpoint
│   │       └── exit_game.py   # Exit game endpoint
│   ├── models/         # Data models
│   ├── services/       # Business logic services
│   └── requirements.txt # Python dependencies
├── docker/             # Docker configuration files
├── __mocks__/          # Jest mock files
├── webpack.config.js   # Webpack configuration
├── tsconfig.json       # TypeScript configuration
├── jest.config.js      # Jest configuration
├── jest.setup.js       # Jest setup file
├── package.json        # NPM dependencies and scripts
├── docker-compose.yml  # Docker Compose configuration for development
└── docker-compose.test.yml  # Docker Compose configuration for tests
```

## Key Components
- **Game Engine**: Phaser 3 for rendering and game logic
- **Scene Management**: Phaser's scene system for game state organization
- **UI Components**: Reusable UI elements for consistent interface
- **Game Views**: Different views for game hierarchy (Startup, Galaxy, System, Planet)
- **API Integration**: Communication with FastAPI backend for game state
- **Asset Loading**: Phaser's loader for game assets

## Data Flow
1. User interacts with the Phaser game UI
2. Game logic processes user input
3. API requests are sent to the FastAPI backend when needed
4. Backend processes game logic and updates data store
5. Updated game state is returned to the frontend
6. UI is updated to reflect the new game state

## External Dependencies
- Phaser 3 for game development
- TypeScript for type-safe JavaScript
- Webpack for bundling
- FastAPI for backend API
- Docker for containerization

## Backend API Endpoints
- `/new-game`: Create a new game with specified parameters
- `/saved-games`: List all saved games
- `/load-game`: Load a saved game by ID
- `/settings`: Get or update game settings
- `/settings/reset`: Reset game settings to defaults
- `/exit`: Handle game exit, optionally saving the game

## Recent Significant Changes
- [2025-03-06] Initial project setup
- [2025-03-06] Implemented basic game UI components and scenes
- [2025-03-06] Added Jest testing framework and created tests for components
- [2025-03-06] Fixed failing tests by removing problematic test case in Panel.test.ts
- [2025-03-06] Created docker-compose.test.yml for running tests in Docker
- [2025-03-06] Established rule to use docker-compose exclusively for running the game and tests
- [2025-03-06] Created FastAPI backend with stub endpoints for start menu options
- [2025-03-06] Fixed backend import error by updating the import path in main.py

## Development Workflow
1. Run `docker-compose up` to start both frontend and backend services
2. Run `docker-compose up frontend` to start only the frontend development server
3. Run `docker-compose up backend` to start only the backend API server
4. Make changes to the code
5. See changes reflected in the browser automatically
6. Access the API documentation at http://localhost:8000/docs
7. Run `docker-compose -f docker-compose.test.yml run frontend` to run the test suite
8. Use `docker-compose -f docker-compose.test.yml run frontend-watch` for watch mode
9. Use `docker-compose -f docker-compose.test.yml run frontend-coverage` for test coverage

## Important Rule
**ONLY use docker-compose for running the game or tests. DO NOT run the game code or tests directly in the console.**

This rule ensures consistency across development environments and simplifies the development workflow.
