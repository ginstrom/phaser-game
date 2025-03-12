"""Main FastAPI application module.
* Initializes FastAPI app with CORS middleware and database
* Sets up API routes for game operations
* Handles application lifecycle with lifespan context manager
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager

# Import database
from app.database.config import engine, Base

# Import routers
from app.routers import new_game, load_game, settings, exit_game, game_entities
from app.routes import game

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Clean up resources if needed
    pass

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
app.include_router(game.router)
app.include_router(game_entities.router, tags=["Game Entities"])

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to the 4X Space Empire API",
        "version": "0.1.0",
        "documentation": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)