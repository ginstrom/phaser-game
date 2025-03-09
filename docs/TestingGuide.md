# Testing Guide for Phaser Game

This document provides comprehensive information about testing in the Phaser Game project.

## Test Structure

The project has two main test suites:

1. **Frontend Tests**: Jest tests for the TypeScript/Phaser frontend
2. **Backend Tests**: Pytest tests for the FastAPI backend

## Running Tests

Always use the `test.sh` script to run tests. This script ensures the proper environment is set up in Docker containers.

### Basic Usage

```bash
# Run frontend tests
./test.sh frontend

# Run backend tests
./test.sh backend

# Run all tests
./test.sh all
```

### Advanced Options

#### Frontend Test Options

```bash
# Run frontend tests in watch mode (automatically re-run on file changes)
./test.sh frontend --watch

# Run frontend tests with coverage report
./test.sh frontend --coverage
```

#### Backend Test Options

```bash
# Run backend tests with verbose output
./test.sh backend --verbose

# Run backend tests with coverage report
./test.sh backend --coverage
```

## How Tests Work

### Frontend Tests

- Uses Jest as the test runner
- Tests are located in `frontend/src/__tests__/`
- Mocks for Phaser are in `frontend/__mocks__/`
- Configuration is in `frontend/jest.config.js`

### Backend Tests

- Uses pytest as the test runner
- Tests are located in `backend/tests/`
- Test configuration is in `backend/pytest.ini`
- Test fixtures are defined in `backend/tests/conftest.py`

### Docker Test Environment

The `docker-compose.test.yml` file defines the test environment:

1. **Frontend Test Container**:
   - Builds from `docker/Dockerfile.frontend`
   - Mounts the frontend directory to `/app`
   - Runs npm test commands

2. **Backend Test Container**:
   - Builds from `docker/Dockerfile.backend`
   - Mounts the backend directory to `/app`
   - Sets `PYTHONPATH=/app` environment variable
   - Runs the `run_tests.sh` script

## Writing Tests

### Frontend Test Guidelines

1. Place test files in `frontend/src/__tests__/` mirroring the structure of the source files
2. Name test files with `.test.ts` extension
3. Use Jest's `describe` and `it` functions for test organization
4. Use the Phaser mocks for testing game components

Example:
```typescript
import { Button } from '../../ui/Button';

describe('Button', () => {
  it('should create a button with the correct text', () => {
    const button = new Button({
      scene: {} as Phaser.Scene,
      x: 100,
      y: 100,
      text: 'Test Button'
    });
    
    expect(button.text).toBe('Test Button');
  });
});
```

### Backend Test Guidelines

1. Place test files in `backend/tests/` with `test_` prefix
2. Use pytest fixtures for common setup
3. Group related tests in the same file
4. Use descriptive test names that explain the behavior being tested

Example:
```python
def test_create_new_game_with_default_values(client):
    """
    Test creating a new game with only the required player_name parameter.
    Default values should be used for difficulty and galaxy_size.
    """
    response = client.post(
        "/new-game",
        json={"player_name": "TestPlayer"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "game_id" in data
    assert data["initial_state"]["player"]["name"] == "TestPlayer"
```

## Troubleshooting

### Common Frontend Test Issues

1. **Module not found errors**:
   - Check that all dependencies are installed in the Docker container
   - Verify import paths are correct (case-sensitive)

2. **Phaser-related errors**:
   - Make sure you're using the Phaser mocks correctly
   - Check that game objects are properly initialized in tests

### Common Backend Test Issues

1. **Import errors**:
   - Ensure all directories have `__init__.py` files
   - Check that `PYTHONPATH` is set correctly in the Docker container
   - Use absolute imports in test files

2. **Database errors**:
   - The test environment uses an in-memory SQLite database
   - Make sure database models are properly defined
   - Check that test fixtures are setting up the database correctly

3. **API response errors**:
   - Verify the expected response structure matches the actual API response
   - Check for changes in the API endpoints that might affect tests

## Continuous Integration

The project uses GitHub Actions for continuous integration:
- Tests are run automatically on pull requests
- Both frontend and backend tests must pass before merging
- Test coverage reports are generated and uploaded as artifacts

## Best Practices

1. **Write tests before code** (Test-Driven Development)
2. **Keep tests independent** - each test should run in isolation
3. **Test edge cases** - not just the happy path
4. **Keep tests fast** - slow tests discourage frequent testing
5. **Use meaningful assertions** - test for specific behaviors
6. **Don't test implementation details** - test behavior, not how it's implemented