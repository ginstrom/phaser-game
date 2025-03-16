# Development Process for Phaser Games

## Adding New Scenes & Entities

### 1. Scene/Entity Implementation
1. **Create New Module:**
   - Create a new scene or game object file in `src/scenes/` or `src/entities/` (e.g., `src/scenes/MainScene.ts` or `src/entities/Player.ts`).
   - Implement the class using TypeScript, extending Phaser’s built-in classes (e.g., `Phaser.Scene`, `Phaser.GameObjects.Sprite`).
   - Define key methods (`preload`, `create`, `update`) for scenes or initialize behavior for entities.
2. **Type Safety & Documentation:**
   - Use TypeScript interfaces for any custom data structures.
   - Document your code, including configuration details and expected interactions.
   - Follow naming conventions:
     - **camelCase:** functions and variables (e.g., `loadAssets`, `isDataReady`)
     - **PascalCase:** classes and scene names (e.g., `MainScene`, `PlayerEntity`)

### 2. Testing
1. **Unit and Integration Tests:**
   - Write tests in `tests/<component-name>.spec.ts` (e.g., `tests/mainScene.spec.ts`, `tests/player.spec.ts`).
   - Test scene initialization, game object behavior, API integration, and any custom logic.
   - Include teardown code to reset the game state after tests.
2. **Run Tests:**
   - Execute tests using your preferred command-line tool (e.g., npm scripts or make commands):
     ```bash
     make test-game
     ```
   - Address any issues until all tests pass.

## API Implementation for Game Data & Logic

### 3. API Service Implementation
1. **Create API Services:**
   - Develop API service modules in `src/api/` (e.g., `src/api/gameDataService.ts`).
   - Implement functions to fetch, cache, and process game data such as levels, scores, and configurations.
   - Use TypeScript interfaces to enforce the structure of API responses.
2. **Integration:**
   - Integrate API calls within your scenes or game logic modules.
   - Ensure API calls are isolated in dedicated services for easier testing and maintenance.
3. **Environment Configuration:**
   - Use environment variables for API endpoints and credentials, ensuring different configurations for development, staging, and production.

### 4. API Testing
1. **Write API Tests:**
   - Add tests in `tests/api.spec.ts` to verify data fetching, error handling, and integration with game logic.
2. **Run API Tests:**
   - Execute API tests with:
     ```bash
     make test-api
     ```
   - Fix issues until tests pass.

## Documentation

### 5. Documentation Tasks
1. **API Documentation:**
   - Update documentation in `docs/game-api.md` to include all API endpoints, request/response examples, and data structure specifications.
2. **Game Components Documentation:**
   - Document your scenes, entities, and game logic in `docs/game-components.md`, including usage examples and design decisions.
3. **Revision History:**
   - Maintain a revision log in `docs/revision_history.md` noting major changes and new additions.
4. **Task Tracking:**
   - Update `docs/current_task.md` to mark completed items, list next steps, and adjust your plan of action as necessary.

## Docker-Compose & Containerization

### 6. Container Setup
1. **Docker Environment:**
   - Ensure your game runs inside a docker-compose setup.
   - Create a `Dockerfile` and a `docker-compose.yml` in the project root.
   - Configure services for the game server, API backend (if separate), and other dependencies.
2. **Environment Variables & Configuration:**
   - Use environment variables to manage configuration across development, staging, and production.
   - Document container setup and instructions in `docs/docker_setup.md`.

### 7. Running in Docker
- **Build the Docker Image:**
  ```bash
  docker-compose build
  ```
- **Start the Containers:**
  ```bash
  docker-compose up
  ```

## Testing

- **Run a Specific Test File:**
  ```bash
  make test-frontend TEST_FILE=tests/<test_file>.spec.ts
  ```
- **Run All Tests:**
  ```bash
  make test-frontend
  ```

## Version Control

1. **Logical Commit Groups:**
   - Group commits into:
     - Scene/Entity and game logic changes
     - API service implementation
     - Tests
     - Documentation
     - Docker and configuration changes
2. **Commit Messages:**
   - Use meaningful commit messages that clearly describe the changes.

## Keeping Documentation Up to Date
- Update all relevant documentation before starting work and after completing changes to ensure consistency with the codebase.

## Wrapping Up

When wrapping up a development session:
- **Finalize Documentation:** Ensure all changes are reflected in your documentation files.
- **Commit Changes:** Commit your changes in logical groupings according to the version control guidelines.

---

This manual should guide you through adding new features and maintaining your Phaser game project while ensuring a modular design, robust API integration, thorough testing, and smooth containerized deployment.