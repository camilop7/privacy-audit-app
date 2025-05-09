from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.schemas.service import ServiceOut
from app.schemas.user import UserOut

class BookingBase(BaseModel):
    service_id: UUID
    scheduled_for: datetime
    status: Optional[str] = "pending"
    notes: Optional[str] = None

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    scheduled_for: Optional[datetime]
    status: Optional[str]
    notes: Optional[str]

class BookingOut(BookingBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    service: ServiceOut
    # optionally include user details:
    # user: UserOut

    class Config:
        orm_mode = True
