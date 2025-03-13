import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# Base class for declarative models
Base = declarative_base()

# Get database URL from environment or default to SQLite
ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")
if ENVIRONMENT == "test":
    DATABASE_URL = "sqlite:///:memory:"
else:
    DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./test.db")

# Create synchronous engine with SQLite-specific config if needed
engine = create_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

# Create synchronous session factory
session_maker = sessionmaker(
    engine,
    expire_on_commit=False
)

# Dependency for FastAPI endpoints to provide a database session
def get_db():
    """
    Creates and yields a new database session.
    Ensures proper cleanup of the session after use.
    
    Yields:
        Session: SQLAlchemy database session
    """
    session = session_maker()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()