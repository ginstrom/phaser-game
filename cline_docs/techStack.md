## Frontend
- Framework: Phaser.js for game scenes
- State Management: Various in-house utilities

## Backend
- Language: Python
- Web Framework: FastAPI
- Database: SQLite with asynchronous support using SQLAlchemy and aiosqlite
- ORM: SQLAlchemy (async) for database operations
- Other Dependencies: Additional libraries as listed in backend/requirements.txt

## DevOps
- Containerization: Docker (all commands and tests run via docker-compose)
- Testing: Pytest (executed through docker-compose for backend tests)

_NOTE: The backend now requires SQLAlchemy to be installed. Ensure that SQLAlchemy is added to backend/requirements.txt so that the docker environment has the correct dependencies._
