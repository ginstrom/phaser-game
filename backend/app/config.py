import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Base class for declarative models
Base = declarative_base()

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