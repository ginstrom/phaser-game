"""Main FastAPI application module.
* Initializes FastAPI app with CORS middleware and database
* Sets up API routes for game operations
* Handles application lifecycle with lifespan context manager
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager
import logging
import os
from alembic.config import Config as AlembicConfig
from alembic import command as alembic_command

# Import database
from app.database.config import engine, Base

# Import routers
from app.routers import new_game, load_game, settings, exit_game, game_entities

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migrations():
    """Run database migrations using the Alembic API."""
    try:
        # Get the project root directory
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        alembic_ini = os.path.join(base_dir, 'alembic.ini')
        
        if not os.path.exists(alembic_ini):
            logger.warning(f"Alembic config not found at {alembic_ini}, skipping migrations")
            return
        
        logger.info(f"Running database migrations from {alembic_ini}")
        
        # Create an Alembic configuration object
        alembic_cfg = AlembicConfig(alembic_ini)
        
        # Run the migration
        alembic_command.upgrade(alembic_cfg, "head")
        logger.info("Database migrations completed successfully")
    except Exception as e:
        logger.error(f"Error running database migrations: {str(e)}")
        # In production, you might want to raise the exception to prevent startup with a bad DB state
        # In development, we'll log and continue

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for the FastAPI application."""
    # Initialize application state
    app.state.environment = os.environ.get("ENVIRONMENT", "development")
    
    # Run database migrations on startup (except in test environment)
    if app.state.environment != "test":
        run_migrations()
    
    logger.info("Application startup complete")
    yield
    logger.info("Application shutdown")

# Create FastAPI app
app = FastAPI(
    title="4X Space Empire API",
    description="Backend API for the 4X Space Empire game",
    version="0.1.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, this should be restricted to the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(new_game.router, tags=["Game"])
app.include_router(load_game.router, tags=["Game"])
app.include_router(settings.router, tags=["Settings"])
app.include_router(exit_game.router, tags=["Game"])
app.include_router(game_entities.router, tags=["Game Entities"])

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Welcome to the 4X Space Empire API",
        "version": "0.1.0",
        "documentation": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)