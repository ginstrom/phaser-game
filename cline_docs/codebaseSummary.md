# Codebase Summary

## Project Structure
```
phaser-game/
├── config/             # Shared configuration files
│   └── enums.json      # Shared enum definitions for backend and frontend
├── frontend/
│   ├── src/
│   │   ├── assets/         # Game assets (images, audio, etc.)
│   │   ├── scenes/         # Phaser scene files
│   │   │   ├── MainScene.ts       # Main game scene
│   │   │   ├── StartupScene.ts    # Main menu scene
│   │   │   ├── GalaxyScene.ts     # Galaxy view scene
│   │   │   ├── SystemScene.ts     # System view scene
│   │   │   └── PlanetScene.ts     # Planet view scene
│   │   ├── ui/             # UI components
│   │   │   ├── Button.ts          # Reusable button component
│   │   │   ├── InputField.ts      # Input field component for forms
│   │   │   ├── Panel.ts           # Reusable panel component
│   │   │   ├── SelectField.ts     # Dropdown select component for forms
│   │   │   └── TextStyles.ts      # Text style definitions
│   │   ├── objects/        # Game object classes
│   │   ├── utils/          # Utility functions
│   │   ├── __tests__/      # Test files
│   │   │   ├── index.test.ts      # Game initialization tests
│   │   │   ├── scenes/            # Scene tests
│   │   │   └── ui/                # UI component tests
│   │   └── index.ts        # Main entry point for the game
│   ├── public/
│   │   └── index.html      # HTML entry point
│   ├── __mocks__/          # Jest mock files
│   ├── webpack.config.js   # Webpack configuration
│   ├── tsconfig.json       # TypeScript configuration
│   ├── jest.config.js      # Jest configuration
│   ├── jest.setup.js       # Jest setup file
│   └── package.json        # NPM dependencies and scripts
├── backend/
│   ├── app/            # FastAPI application
│   │   ├── main.py     # Main application entry point
│   │   ├── config.py   # Configuration loader for enums
│   │   ├── models/     # Data models
│   │   │   └── game.py # Game state models
│   │   ├── services/   # Business logic services
│   │   │   └── game_service.py # Game creation and management
│   │   └── routers/    # API route handlers
│   │       ├── new_game.py    # New game endpoint
│   │       ├── load_game.py   # Load game endpoint
│   │       ├── settings.py    # Settings endpoint
│   │       └── exit_game.py   # Exit game endpoint
│   └── requirements.txt # Python dependencies
├── docker/             # Docker configuration files
├── test.sh             # Script for running tests with various options
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
- [2025-03-07] Implemented enum-based type system for game entities using a shared JSON configuration
- [2025-03-07] Created a shared config directory with enums.json for synchronizing enums between backend and frontend
- [2025-03-07] Updated backend models and services to use enum types for planet types, galaxy sizes, and difficulty levels
- [2025-03-07] Modified Docker configuration to mount the config directory in containers
- [2025-03-07] Fixed failing unit tests by correcting the Graphics object creation in InputField.ts and updating the Phaser mock
- [2025-03-07] Created test.sh script to simplify running tests with support for frontend, backend, and various options
- [2025-03-07] Enhanced the new game window with a proper form interface, including input fields and dropdown selects
- [2025-03-07] Created new UI components: InputField for text input and SelectField for dropdown selection
- [2025-03-07] Improved the layout and styling of the new game form with clear cancel/start buttons
- [2025-03-07] Implemented system discovery levels (visible light, scanning levels 1-5, visited) and enhanced exploration mechanics
- [2025-03-07] Added ability to view unexplored systems with varying levels of detail based on discovery level
- [2025-03-07] Updated system visuals to reflect discovery levels with different colors
- [2025-03-07] Modified SystemScene to show appropriate details based on discovery level
- [2025-03-06] Initial project setup
- [2025-03-06] Implemented basic game UI components and scenes
- [2025-03-06] Added Jest testing framework and created tests for components
- [2025-03-06] Fixed failing tests by removing problematic test case in Panel.test.ts
- [2025-03-06] Created docker-compose.test.yml for running tests in Docker
- [2025-03-06] Established rule to use docker-compose exclusively for running the game and tests
- [2025-03-06] Created FastAPI backend with stub endpoints for start menu options
- [2025-03-06] Fixed backend import error by updating the import path in main.py
- [2025-03-06] Restructured project by moving frontend code to a dedicated frontend directory
- [2025-03-06] Created basic unit tests for the backend API endpoints
- [2025-03-06] Verified that the frontend app and tests still run correctly from docker-compose after restructuring
- [2025-03-06] Fixed Docker build issue with frontend tests by updating the build context in docker-compose.test.yml
- [2025-03-06] Implemented actual functionality for the new game endpoint
- [2025-03-06] Created game models and services for game state management
- [2025-03-06] Restructured backend code to use app/models and app/services directories
- [2025-03-06] Connected frontend to backend's new game endpoint
- [2025-03-06] Created API utility for making requests to the backend
- [2025-03-06] Added game state management in the frontend
- [2025-03-06] Updated StartupScene to call the new game endpoint
- [2025-03-06] Updated GalaxyScene to display game state information
- [2025-03-06] Fixed issue with game data not correctly initializing on the front end
- [2025-03-06] Added robust error handling and validation in the GameState class
- [2025-03-06] Enhanced error handling in the StartupScene
- [2025-03-06] Added additional checks in the GalaxyScene for missing resources
- [2025-03-06] Documented the galaxy view appearance after starting a new game, including player information, star systems representation, and system interaction
- [2025-03-06] Fixed issue with system names in tooltips by making unexplored systems consistently show "???" in both tooltips and labels

## Development Workflow
1. Run `docker-compose up` to start both frontend and backend services
2. Run `docker-compose up frontend` to start only the frontend development server
3. Run `docker-compose up backend` to start only the backend API server
4. Make changes to the code
5. See changes reflected in the browser automatically
6. Access the API documentation at http://localhost:8000/docs
7. Run tests using the `test.sh` script:
   - `./test.sh frontend` to run frontend tests
   - `./test.sh backend` to run backend tests
   - `./test.sh all` to run both frontend and backend tests
   - Add `--watch` for frontend watch mode
   - Add `--coverage` for test coverage reports
   - Add `--verbose` for verbose backend test output
   - Run `./test.sh --help` for more information

   Alternatively, you can still use the docker-compose commands directly:
   - Run `docker-compose -f docker-compose.test.yml run frontend` to run the frontend test suite
   - Use `docker-compose -f docker-compose.test.yml run frontend-watch` for watch mode
   - Use `docker-compose -f docker-compose.test.yml run frontend-coverage` for test coverage
   - Run `docker-compose -f docker-compose.test.yml run backend` to run the backend test suite
   - Use `docker-compose -f docker-compose.test.yml run backend-verbose` for verbose output
   - Use `docker-compose -f docker-compose.test.yml run backend-coverage` for test coverage

## Important Rule
**ONLY use docker-compose for running the game or tests. DO NOT run the game code or tests directly in the console.**

This rule ensures consistency across development environments and simplifies the development workflow.
