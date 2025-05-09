from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from uuid import UUID

from app.schemas.booking import (
    BookingCreate, BookingUpdate, BookingOut
)
from app.crud import booking as crud_booking
from app.db.session import get_db
from app.core.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[BookingOut])
def list_bookings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud_booking.get_bookings(db, skip, limit)

@router.post(
    "/",
    response_model=BookingOut,
    status_code=status.HTTP_201_CREATED
)
def create_booking(
    bkin: BookingCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud_booking.create_booking(db, bkin, current_user.id)

@router.get("/{booking_id}", response_model=BookingOut)
def get_booking(booking_id: UUID, db: Session = Depends(get_db)):
    bk = crud_booking.get_booking(db, booking_id)
    if not bk:
        raise HTTPException(status_code=404, detail="Booking not found")
    return bk

@router.put("/{booking_id}", response_model=BookingOut)
def update_booking(
    booking_id: UUID,
    bkupd: BookingUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    bk = crud_booking.get_booking(db, booking_id)
    if not bk or bk.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Booking not found")
    return crud_booking.update_booking(db, booking_id, bkupd)

@router.delete("/{booking_id}", response_model=BookingOut)
def delete_booking(
    booking_id: UUID,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    bk = crud_booking.get_booking(db, booking_id)
    if not bk or bk.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Booking not found")
    return crud_booking.delete_booking(db, booking_id)
