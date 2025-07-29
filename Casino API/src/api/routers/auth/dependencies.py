from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.api.db.database import engine

from contextlib import asynccontextmanager

# создаем асинхронную фабрику сессий
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# сам генератор сессий
@asynccontextmanager
async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session