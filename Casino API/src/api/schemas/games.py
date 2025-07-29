from datetime import datetime

from pydantic import BaseModel

class GameRoundCreate(BaseModel):
    user_id: int
    bet_amount: int

class GameRoundOut(BaseModel):
    id: int
    user_id: int
    bet_amount: int
    win_amount: int
    is_win: bool
    created_at: datetime