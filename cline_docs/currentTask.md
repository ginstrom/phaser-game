## Current Task

- Integrate the asynchronous SQLAlchemy setup into the existing backend service.
- Update necessary modules (database configuration, repositories, and service functions) to use the new async approach.
- Ensure minimal disruption by only modifying code that directly interacts with the database layer.
- Verify functionality by running tests in the proper docker-compose environment.

### IMPORTANT REMINDER
Always run your code and tests using docker-compose (e.g., via `docker-compose up` or appropriate commands) to ensure that the environment is consistent and reliable. This practice helps avoid issues caused by local setup discrepancies and ensures that the integrated changes work correctly in the containerized environment.

## Next Steps
1. Deploy changes using docker-compose.
2. Run tests with the docker-compose setup.
3. Verify that asynchronous database calls function correctly in both PostgreSQL and SQLite environments.
