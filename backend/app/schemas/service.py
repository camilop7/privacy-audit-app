from pydantic import BaseModel, constr
from typing import Optional
from uuid import UUID
from datetime import datetime

class ServiceBase(BaseModel):
    name: constr(max_length=255)
    description: Optional[str] = None
    category: Optional[constr(max_length=100)] = None
    price: float
    duration_minutes: float

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    name: Optional[constr(max_length=255)]
    description: Optional[str]
    category: Optional[constr(max_length=100)]
    price: Optional[float]
    duration_minutes: Optional[float]

class ServiceOut(ServiceBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
