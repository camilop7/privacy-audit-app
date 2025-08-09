from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, func, and_, or_

from app.db.session import get_db
from app.models.booking import Booking, BookingStatus
from app.models.service import Service
from app.models.user import User, UserRole
from app.schemas.booking import BookingCreate, BookingUpdate, BookingRead, Page
from app.core.security import get_current_active_user

router = APIRouter(prefix="/bookings", tags=["bookings"])

# ---- helpers ----

ALLOWED_TRANSITIONS = {
    BookingStatus.pending: {BookingStatus.confirmed, BookingStatus.cancelled},
    BookingStatus.confirmed: {BookingStatus.completed, BookingStatus.cancelled},
    BookingStatus.completed: set(),
    BookingStatus.cancelled: set(),
}


def _assert_transition(old: BookingStatus, new: BookingStatus):
    if new not in ALLOWED_TRANSITIONS[old]:
        raise HTTPException(status_code=400, detail=f"Illegal status change {old} → {new}")


def _is_admin(user: User) -> bool:
    return user.role in {UserRole.admin, UserRole.analyst}

# ---- endpoints ----

@router.get("/", response_model=Page)
def list_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    status: Optional[BookingStatus] = Query(None),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    limit: int = Query(25, ge=1, le=200),
    offset: int = Query(0, ge=0),
    q: Optional[str] = Query(None, description="search notes or service name"),
):
    stmt = select(Booking)

    if not _is_admin(current_user):
        stmt = stmt.where(Booking.user_id == current_user.id)

    if status:
        stmt = stmt.where(Booking.status == status)

    if date_from:
        stmt = stmt.where(Booking.start_time >= date_from)
    if date_to:
        stmt = stmt.where(Booking.end_time <= date_to)

    if q:
        # naive search on notes; could join Service for name
        stmt = stmt.where(or_(Booking.notes.ilike(f"%{q}%")))

    total = db.execute(select(func.count()).select_from(stmt.subquery())).scalar_one()

    stmt = stmt.order_by(Booking.start_time.desc()).limit(limit).offset(offset)
    rows = db.execute(stmt).scalars().all()

    items = []
    for b in rows:
        items.append(
            BookingRead(
                id=b.id,
                user_id=b.user_id,
                service_id=b.service_id,
                status=b.status,
                start_time=b.start_time,
                end_time=b.end_time,
                price_at_booking=b.price_at_booking,
                created_at=b.created_at,
                updated_at=b.updated_at,
                service_name=getattr(b.service, "name", None),
            )
        )

    return Page(items=items, total=total)


@router.post("/", response_model=BookingRead, status_code=201)
def create_booking(data: BookingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if data.end_time <= data.start_time:
        raise HTTPException(status_code=400, detail="end_time must be after start_time")

    svc = db.get(Service, data.service_id)
    if not svc:
        raise HTTPException(status_code=404, detail="Service not found")

    booking = Booking(
        user_id=current_user.id,
        service_id=svc.id,
        start_time=data.start_time,
        end_time=data.end_time,
        status=BookingStatus.pending,
        notes=data.notes,
        price_at_booking=svc.price,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)

    return BookingRead(
        id=booking.id,
        user_id=booking.user_id,
        service_id=booking.service_id,
        status=booking.status,
        start_time=booking.start_time,
        end_time=booking.end_time,
        price_at_booking=booking.price_at_booking,
        created_at=booking.created_at,
        updated_at=booking.updated_at,
        service_name=svc.name,
    )


@router.get("/{booking_id}", response_model=BookingRead)
def get_booking(booking_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    booking = db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if not _is_admin(current_user) and booking.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    return BookingRead.model_validate(booking, from_attributes=True)


@router.patch("/{booking_id}", response_model=BookingRead)
def update_booking(booking_id: UUID, data: BookingUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    booking = db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if not _is_admin(current_user) and booking.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    if data.status and data.status != booking.status:
        _assert_transition(booking.status, data.status)
        booking.status = data.status

    if data.start_time:
        booking.start_time = data.start_time
    if data.end_time:
        if data.end_time <= (data.start_time or booking.start_time):
            raise HTTPException(status_code=400, detail="end_time must be after start_time")
        booking.end_time = data.end_time

    if data.notes is not None:
        booking.notes = data.notes

    db.commit()
    db.refresh(booking)
    return BookingRead.model_validate(booking, from_attributes=True)


@router.delete("/{booking_id}", status_code=204)
def delete_booking(booking_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    booking = db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if not _is_admin(current_user) and booking.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    if booking.status not in {BookingStatus.pending, BookingStatus.cancelled} and not _is_admin(current_user):
        raise HTTPException(status_code=400, detail="Only pending/cancelled bookings can be deleted by users")

    db.delete(booking)
    db.commit()
    return None
