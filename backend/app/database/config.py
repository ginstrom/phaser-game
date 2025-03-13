"""Configuration module for database and session management.
* Sets up SQLAlchemy database connection and base model
* Provides consistent database session management across environments
* Supports both SQLite and PostgreSQL databases
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# Base class for declarative models
Base = declarative_base()

# Get database URL from environment or default to SQLite
ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")

# Configure database URLs per environment
if ENVIRONMENT == "test":
    DATABASE_URL = "sqlite:///:memory:"
elif ENVIRONMENT == "development":
    DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./dev.db")
else:  # production
    # Production should use PostgreSQL
    DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@db:5432/space_empire_db")

# Configure connection args based on database type
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

# Create engine with appropriate config
engine = create_engine(
    DATABASE_URL,
    echo=ENVIRONMENT == "development",  # Echo SQL in development only
    future=True,
    connect_args=connect_args
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Dependency for FastAPI endpoints to provide a database session
def get_db():
    """
    Creates and yields a new database session.
    Ensures proper cleanup of the session after use.
    
    Yields:
        Session: SQLAlchemy database session
    """
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()