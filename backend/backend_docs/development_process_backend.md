# Development Process

## Adding New Models

### 1. Model Implementation
1. Create the model class in `backend/<app-name>/models.py`
   - Define fields with appropriate types and constraints
   - Add string representation method
   - Include Meta class with app_label
   - Document field choices and constraints in code

### 2. Testing
1. Add model tests in `backend/<app-name>/tests/test_models.py`
   - Test model creation with valid data
   - Test validation constraints
   - Test string representation
   - Test any enums or choices
   - Write teardown/cleanup code to remove any data added to the db by tests.
2. Run tests using make command:
   ```bash
   make backend-shell python manage.py test <app-name>.tests.test_models
   ```
3. Fix any issues until tests pass

### 3. API Implementation
1. Add serializer in `backend/<app-name>/serializers.py`
   - Define fields that need special handling
   - Set up field validation if needed
2. Add ViewSet in `backend/<app-name>/views.py`
   - Implement any custom logic needed
3. Update URL routing in `backend/<app-name>/urls.py`
   - Add new ViewSet to router

### 4. API Testing
1. Add API tests in `backend/<app-name>/tests/test_api.py`
   - Test CRUD operations
   - Test validation errors
   - Test any custom endpoints
2. Run API tests:
   ```bash
   make backend-shell python manage.py test <app-name>.tests.test_api
   ```
3. Fix any issues until tests pass

### 5. Documentation
1. Update API documentation in `backend/backend_docs/api.md`
   - Document all endpoints
   - Include request/response examples
   - Document field specifications
2. Update models documentation in `backend/backend_docs/models.md`
   - Document model fields and relationships
   - Include usage examples
   - Document implementation details
3. Update revision history in `backend/backend_docs/revision_history.md`
   - Add entry for new model
   - List all major changes
4. Update current task in `backend/backend_docs/current_task.md`
   - Mark completed items
   - Update next steps
   - Revise plan of action

### 6. Version Control
    Commit changes in accordance with Version Control rules.

### Important Notes
- Always use `make backend-shell` for running commands
- Follow test-driven development practices
- Keep documentation in sync with code changes
- Use meaningful commit messages
- Review this process document before starting new model implementation

## Database Migrations
1. Create migration:
   ```bash
   make backend-shell python manage.py makemigrations <app-name>
   ```
2. Apply migration:
   ```bash
   make backend-shell python manage.py migrate <app-name>
   ```

## Testing
- Run specific test file:
  ```bash
  make backend-shell python manage.py test <app-name>.tests.<test_file>
  ```
- Run all tests for an app:
  ```bash
  make backend-shell python manage.py test <app-name>
  ```
- Run all tests for the backend:
  ```bash
  make test-backend
  ```

## Version Control
1. Commit changes in logical groups:
   - Model and migrations
   - API implementation
   - Tests
   - Documentation

## Keeping Documentation up to Date
Perform your documentation tasks before starting work, and after you are finished.

## Wrapping Up

When you are asked to wrap up, follow these steps in order:

1. Run Tests
   ```bash
   make backend-shell python manage.py test <app-name>.tests.<test_file>
   ```
   - Verify all tests pass
   - Fix any failing tests before proceeding

2. Update Documentation
   - Update revision history in `backend/backend_docs/revision_history.md`
     - Add a new entry at the top with today's date
     - Include a clear title describing the feature/change
     - List all major changes and improvements
     - Note any important implementation details
   - Update relevant documentation files (models.md, api.md, etc.)
   - Update current_task.md if needed

3. Stage Changes
   ```bash
   git add <modified-files>
   ```
   - Stage all modified files
   - Group related changes together
   - Include all documentation updates

4. Commit Changes
   ```bash
   git commit -m "<type>: <description>"
   ```
   - Use conventional commit types (feat, fix, refactor, etc.)
   - Write clear, descriptive commit messages
   - Include relevant issue numbers if applicable

5. Verify Changes
   - Review the commit to ensure all changes are included
   - Check that documentation is complete and accurate
   - Ensure no sensitive data or temporary files were committed

### Example Wrap-up
```bash
# 1. Run tests
make backend-shell python manage.py test play.tests.test_game_start

# 2. Stage changes
git add backend/play/start.py
git add backend/play/tests/test_game_start.py
git add backend/backend_docs/revision_history.md

# 3. Commit changes
git commit -m "feat: add terran planet and asteroid belt to star system creation"
```

### Important Notes
- Always run tests before committing
- Keep documentation up to date with code changes
- Use meaningful commit messages
- Group related changes together
- Review changes before committing
- Follow the established commit message format