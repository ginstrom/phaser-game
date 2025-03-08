import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.config import get_db
from app.models.game import Base

# Configure in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def override_get_db():
    async with TestSessionLocal() as session:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    """
    Create a test client for the FastAPI application.
    This fixture can be used in tests to make requests to the API.
    """
    return TestClient(app)
