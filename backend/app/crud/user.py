from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.schemas.user import UserCreate
from uuid import UUID
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Utility
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Create new user
def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hash_password(user.password),
        role=user.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Get user by ID
def get_user(db: Session, user_id: UUID) -> User:
    return db.query(User).filter(User.id == user_id).first()

# Get user by email
def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

# Get all users (admin only)
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

# Update user login timestamp
def update_last_login(db: Session, user: User):
    user.last_login = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user

# Delete user
def delete_user(db: Session, user_id: UUID):
    user = get_user(db, user_id)
    if user:
        db.delete(user)
        db.commit()
    return user
