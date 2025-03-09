from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Union
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.config import get_db

router = APIRouter()

class ExitGameRequest(BaseModel):
    save_before_exit: bool = True
    save_name: Optional[str] = None

class ExitGameSavedResponse(BaseModel):
    message: str
    saved: bool = True
    save_id: str

class ExitGameNotSavedResponse(BaseModel):
    message: str
    saved: bool = False

# Union type for the response
ExitGameResponse = Union[ExitGameSavedResponse, ExitGameNotSavedResponse]

@router.post("/exit", response_model=ExitGameResponse)
async def exit_game(request: ExitGameRequest, db: AsyncSession = Depends(get_db)):
    """
    Handle game exit, optionally saving the game before exiting.
    
    This is a stub endpoint that will be implemented with actual exit logic in the future.
    In a real implementation, this might save the game state to a database if requested.
    
    Note: In a browser-based game, the actual exit functionality would be handled by the client,
    but this endpoint can be used to perform server-side cleanup and saving.
    """
    try:
        # Stub implementation
        if request.save_before_exit:
            # Mock saving the game
            save_id = "save-" + (request.save_name or "auto-exit").replace(" ", "-").lower()
            
            return {
                "message": f"Game saved as '{request.save_name or 'Auto-Exit Save'}' before exit",
                "saved": True,
                "save_id": save_id
            }
        else:
            return {
                "message": "Game exited without saving",
                "saved": False
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process exit request: {str(e)}")