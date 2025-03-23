from pydantic import BaseModel, EmailStr
from typing import Optional
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    analyst = "analyst"
    user = "user"

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str
    role: Optional[UserRole] = UserRole.user

class UserLogin(BaseModel):
    email: EmailStr
    password: str
