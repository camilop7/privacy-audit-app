from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.models.booking import Booking
from app.schemas.booking import BookingCreate, BookingUpdate

def get_booking(db: Session, booking_id: UUID) -> Booking:
    return db.query(Booking).filter(Booking.id == booking_id).first()

def get_bookings(db: Session, skip: int = 0, limit: int = 100) -> List[Booking]:
    return db.query(Booking).offset(skip).limit(limit).all()

def create_booking(db: Session, booking: BookingCreate, user_id: UUID) -> Booking:
    db_booking = Booking(**booking.dict(), user_id=user_id)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def update_booking(
    db: Session, booking_id: UUID, booking_update: BookingUpdate
) -> Booking:
    bk = get_booking(db, booking_id)
    if not bk:
        return None
    for field, value in booking_update.dict(exclude_unset=True).items():
        setattr(bk, field, value)
    db.commit()
    db.refresh(bk)
    return bk

def delete_booking(db: Session, booking_id: UUID) -> Booking:
    bk = get_booking(db, booking_id)
    if bk:
        db.delete(bk)
        db.commit()
    return bk
