from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    balance: int

    class Config:
        from_attributes = True

class UserLogin(BaseModel):

    email: EmailStr
    password: str
