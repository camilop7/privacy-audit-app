from datetime import datetime
from enum import Enum
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class BookingStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"

class BookingBase(BaseModel):
    service_id: UUID
    start_time: datetime
    end_time: datetime
    notes: Optional[str] = None

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[BookingStatus] = None
    notes: Optional[str] = None

class BookingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    service_id: UUID
    status: BookingStatus
    start_time: datetime
    end_time: datetime
    price_at_booking: float
    created_at: datetime
    updated_at: datetime

    # helpful denorms for UI
    service_name: Optional[str] = None

class Page(BaseModel):
    items: List[BookingRead]
    total: int
