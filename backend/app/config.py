"""Configuration module for database and game enums.
* Sets up SQLAlchemy database connection and base model
* Defines game enums (PlanetType, GalaxySize, Difficulty) shared with frontend
* Provides database session management utilities
"""

import os
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from enum import Enum
from pathlib import Path

# Base class for declarative models
Base = declarative_base()

# Load shared enums from JSON
ENUMS_PATH = Path("/config/enums.json")
with open(ENUMS_PATH) as f:
    SHARED_ENUMS = json.load(f)

class PlanetType(str, Enum):
    """Planet types loaded from shared enums"""
    def _generate_next_value_(name, start, count, last_values):
        return name
    
    @classmethod
    def _missing_(cls, value):
        # Handle case-insensitive lookup
        try:
            return cls[value.upper()]
        except KeyError:
            return None

    # Dynamically create enum values from shared JSON
    locals().update({name.upper(): name for name in SHARED_ENUMS["PlanetType"]})

class GalaxySize(str, Enum):
    """Galaxy sizes loaded from shared enums"""
    def _generate_next_value_(name, start, count, last_values):
        return name
    
    @classmethod
    def _missing_(cls, value):
        try:
            return cls[value.upper()]
        except KeyError:
            return None

    # Dynamically create enum values from shared JSON
    locals().update({name.upper(): name for name in SHARED_ENUMS["GalaxySize"]})

class Difficulty(str, Enum):
    """Difficulty levels loaded from shared enums"""
    def _generate_next_value_(name, start, count, last_values):
        return name
    
    @classmethod
    def _missing_(cls, value):
        try:
            return cls[value.upper()]
        except KeyError:
            return None

    # Dynamically create enum values from shared JSON
    locals().update({name.upper(): name for name in SHARED_ENUMS["Difficulty"]})

# Get database URL from environment or default to SQLite
ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")
if ENVIRONMENT == "test":
    DATABASE_URL = "sqlite:///:memory:"
else:
    DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./test.db")

# Create engine with SQLite-specific config if needed
engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

# Create session factory
SessionLocal = sessionmaker(bind=engine)

# Dependency for FastAPI endpoints to provide a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()