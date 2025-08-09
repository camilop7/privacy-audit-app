# app/models/booking.py
from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid, enum

from app.db.base_class import Base

class BookingStatus(str, enum.Enum):
    pending   = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    service_id = Column(UUID(as_uuid=True), ForeignKey("services.id", ondelete="RESTRICT"), nullable=False)

    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time   = Column(DateTime(timezone=True), nullable=False)

    # Keep the desired new type name to match the migration we’re about to fix
    status = Column(Enum(BookingStatus, name="booking_status"), nullable=False, default=BookingStatus.pending)

    notes = Column(String, nullable=True)
    price_at_booking = Column(Float, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", back_populates="bookings")
    service = relationship("Service", lazy="joined")
