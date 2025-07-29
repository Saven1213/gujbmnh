from datetime import datetime
from enum import unique
from time import timezone
from sqlalchemy import DateTime

from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.api.db.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    balance: Mapped[int] = mapped_column(Integer, default=0)
    hashed_password: Mapped[str] = mapped_column(String)


class GameRound(Base):

    __tablename__ = 'gameround'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    bet_amount: Mapped[int] = mapped_column(Integer)
    win_amount: Mapped[int] = mapped_column(Integer)
    is_win: Mapped[bool] = mapped_column(Boolean)
    created_ad: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow
    )

