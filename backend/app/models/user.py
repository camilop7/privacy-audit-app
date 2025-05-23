from sqlalchemy import Column, String, DateTime, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import enum
import uuid

from app.db.session import Base

class UserRole(str, enum.Enum):
    admin = "admin"
    analyst = "analyst"
    user = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    username = Column(String, unique=True, index=True)
    role = Column(Enum(UserRole), default=UserRole.user)

    # New attributes
    full_name = Column(String)
    phone = Column(String)
    address = Column(String)
    company = Column(String)
    job_title = Column(String)
    bio = Column(String)
    profile_picture = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
