from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.models.user import UserRole

# Shared base schema
class UserBase(BaseModel):
    email: EmailStr
    username: str
    role: UserRole = UserRole.user

# For user creation
class UserCreate(UserBase):
    password: str  # plain password input

# For DB return or API response
class UserOut(UserBase):
    id: UUID
    created_at: datetime
    last_login: Optional[datetime]

    class Config:
        orm_mode = True

# For login (optional use)
class UserLogin(BaseModel):
    email: EmailStr
    password: str
