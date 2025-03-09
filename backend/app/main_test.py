from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import database with relative imports for testing
from database.config import engine, Base

# Import routers with relative imports for testing
from routers import new_game, load_game, settings, exit_game

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
def root():
    return {
        "message": "Welcome to the 4X Space Empire API",
        "version": "0.1.0",
        "documentation": "/docs"
    }

# Create tables on startup
@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run("app.main_test:app", host="0.0.0.0", port=8000, reload=True)