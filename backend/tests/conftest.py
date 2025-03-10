import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the app and models
from app.main import app
from app.database.config import get_db, Base

# Configure in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

# Create engine with special SQLite settings for testing
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={
        "check_same_thread": False
    },
    poolclass=StaticPool,  # Use static pool to maintain connections
    echo=True
)

# Create session factory
TestSessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

@pytest.fixture(scope="function", autouse=True)
def setup_test_database():
    """Create tables before each test and drop them after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()

def override_get_db():
    """Override the database dependency for tests."""
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()

# Override the database dependency
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def client(setup_test_database):
    """Create a test client with a fresh database."""
    with TestClient(app) as test_client:
        yield test_client
