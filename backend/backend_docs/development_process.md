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