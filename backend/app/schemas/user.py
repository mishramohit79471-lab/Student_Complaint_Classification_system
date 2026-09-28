from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from app.models.user import UserRole

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.STUDENT

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class TokenData(BaseModel):
    email: Optional[str] = None
