from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.game import Game  # Adjust the import if your model name differs

class GameRepository:
    """Repository for game operations."""
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_game(self, game_data: dict):
        game = Game(**game_data)
        self.session.add(game)
        await self.session.flush()
        return game

    async def get_game_by_id(self, game_id: str):
        result = await self.session.execute(
            select(Game).where(Game.id == game_id)
        )
        return result.scalars().first()
