from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio

# Import database
from app.database.config import engine, Base

# Import routers
from app.routers import new_game, load_game, settings, exit_game

# Create FastAPI app
app = FastAPI(
    title="4X Space Empire API",
    description="Backend API for the 4X Space Empire game",
    version="0.1.0"
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

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to the 4X Space Empire API",
        "version": "0.1.0",
        "documentation": "/docs"
    }

# Create tables on startup
@app.on_event("startup")
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)