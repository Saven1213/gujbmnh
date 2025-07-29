import asyncio
from src.api.db.database import engine, Base

from src.api.models.models import User, GameRound

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_db())