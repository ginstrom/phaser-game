# Backend Test Debugging

## Issue Description
The backend tests are failing with an import error: `ModuleNotFoundError: No module named 'app.main'` in the conftest.py file. This is preventing the tests from running properly in the Docker container.

## Root Cause Analysis
The issue appears to be related to how Python module imports work in the Docker container environment when running pytest. While direct Python script execution can import the app module correctly, pytest has a different import mechanism that's causing the failure.

## Approaches Tried

### 1. Modified conftest.py with different Python path configurations
- Added the parent directory to sys.path
- Added the current working directory to sys.path
- Tried different combinations of path manipulations
- Attempted to use relative imports instead of absolute imports

### 2. Modified docker-compose.test.yml
- Added PYTHONPATH environment variable to include /app
- Changed the command to run pytest from a specific directory
- Created a bash wrapper (run_tests.sh) to set the PYTHONPATH and run the tests

### 3. Created diagnostic scripts
- Created debug_path.py to print Python path information
- Created test_app.py that successfully imports the app module when run directly
- Verified that the app module can be imported correctly in a direct Python script

### 4. Rebuilt the Docker image
- Ensured all required packages were installed (aiosqlite, asyncpg)
- Verified that the Docker container has the correct file structure

### 5. Created a proper Python package
- Added __init__.py file to the backend directory to make it a proper Python package

## Key Findings
- The app module can be imported correctly when running a script directly in the Docker container
- The issue is specifically with how pytest is running the tests
- The Python path in the Docker container includes /app, but pytest is not finding the app module
- The error occurs during the conftest.py loading phase, before any tests are actually run

## Potential Solutions
1. Restructure the project to use a more standard Python package layout
2. Modify the pytest configuration to include the correct paths
3. Use a custom pytest plugin to modify the import mechanism
4. Create a custom test runner that sets up the correct environment before running pytest

## Next Steps
The most promising approach appears to be modifying the pytest configuration and ensuring the project structure follows Python package best practices. This would involve:

1. Ensuring all directories have proper __init__.py files
2. Setting the PYTHONPATH correctly in the Docker container
3. Using a consistent import strategy throughout the codebase