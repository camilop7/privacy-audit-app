from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.db.base_class import Base

class Service(Base):
    __tablename__ = "services"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String)
    category = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    duration_minutes = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
