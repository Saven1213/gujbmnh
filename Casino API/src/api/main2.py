print("Loading main2.py")

from fastapi import FastAPI, APIRouter, Depends
from pydantic import BaseModel, EmailStr

app = FastAPI()
router = APIRouter(prefix="/auth", tags=["Авторизация"])

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

@router.post("/register", response_model=UserOut)
async def register_user(user: UserCreate):
    return UserOut(id=1, email=user.email)

app.include_router(router)

print("Starting FastAPI app...")