from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.routers.auth.dependencies import get_async_session
from src.api.models.models import User
from src.api.schemas.user import UserCreate, UserOut, UserLogin
from src.api.routers.auth.security import verify_password, hash_password, create_access_token
from sqlalchemy import select
from datetime import timedelta

router = APIRouter(
    prefix="/auth",
    tags=["Авторизация"]
)


@router.post('/register', response_model=UserOut)
async def register_user(user: UserCreate, session: AsyncSession = Depends(get_async_session)):

    result = await session.execute(select(User).where(User.email == user.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail='Пользователь уже существует')

    hashed_password = hash_password(user.password)

    new_user = User(username=user.username, hashed_password=hashed_password)

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user

@router.post('/login')
async def login_user(user_data: UserLogin, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User).where(User.email == user_data.email))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверный пароль")

    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=30)
    )

    return {"access_token": access_token, "token_type": "bearer"}