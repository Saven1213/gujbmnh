from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.api.models.models import User
from src.api.schemas.user import UserCreate

async def create_user(db: AsyncSession, user: UserCreate) -> User:
    new_user = User(username=user.username)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_user_by_userbame(db: AsyncSession, username: str) -> User:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()