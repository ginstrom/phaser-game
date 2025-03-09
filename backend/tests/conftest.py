import os
import sys
import pytest
import importlib.util
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Simplify the import approach based on debug findings
# The debug script showed that app.main can be imported directly
# when the Python path is set correctly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the app
import app.main
app = app.main.app
from app.database.config import get_db, Base

# Configure in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

# Create synchronous engine
engine = create_engine(
    TEST_DATABASE_URL,
    future=True,
    echo=True,
    connect_args={"check_same_thread": False}
)

# Create synchronous session factory
TestSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False
)

# Create tables before tests
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Create the tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    # Drop the tables after tests complete
    Base.metadata.drop_all(bind=engine)

# Override the get_db dependency for tests
def override_get_db():
    session = TestSessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client(setup_database):
    """
    Create a test client for the FastAPI application.
    This fixture can be used in tests to make requests to the API.
    """
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def db():
    """
    Create a database session for tests.
    This fixture can be used in tests to access the database directly.
    """
    session = TestSessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
