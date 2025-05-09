from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.models.service import Service
from app.schemas.service import ServiceCreate, ServiceUpdate

def get_service(db: Session, service_id: UUID) -> Service:
    return db.query(Service).filter(Service.id == service_id).first()

def get_services(db: Session, skip: int = 0, limit: int = 100) -> List[Service]:
    return db.query(Service).offset(skip).limit(limit).all()

def create_service(db: Session, svc: ServiceCreate) -> Service:
    db_svc = Service(**svc.dict())
    db.add(db_svc)
    db.commit()
    db.refresh(db_svc)
    return db_svc

def update_service(
    db: Session, service_id: UUID, svc_update: ServiceUpdate
) -> Service:
    svc = get_service(db, service_id)
    if not svc:
        return None
    for field, value in svc_update.dict(exclude_unset=True).items():
        setattr(svc, field, value)
    db.commit()
    db.refresh(svc)
    return svc

def delete_service(db: Session, service_id: UUID) -> Service:
    svc = get_service(db, service_id)
    if svc:
        db.delete(svc)
        db.commit()
    return svc
