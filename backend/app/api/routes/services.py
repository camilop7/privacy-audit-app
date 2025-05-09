from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from uuid import UUID

from app.schemas.service import (
    ServiceCreate, ServiceUpdate, ServiceOut
)
from app.crud import service as crud_service
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=List[ServiceOut])
def list_services(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud_service.get_services(db, skip, limit)

@router.post(
    "/",
    response_model=ServiceOut,
    status_code=status.HTTP_201_CREATED
)
def create_service(
    svc: ServiceCreate,
    db: Session = Depends(get_db)
):
    return crud_service.create_service(db, svc)

@router.get("/{service_id}", response_model=ServiceOut)
def get_service(service_id: UUID, db: Session = Depends(get_db)):
    svc = crud_service.get_service(db, service_id)
    if not svc:
        raise HTTPException(status_code=404, detail="Service not found")
    return svc

@router.put("/{service_id}", response_model=ServiceOut)
def update_service(
    service_id: UUID,
    svc_update: ServiceUpdate,
    db: Session = Depends(get_db)
):
    svc = crud_service.update_service(db, service_id, svc_update)
    if not svc:
        raise HTTPException(status_code=404, detail="Service not found")
    return svc

@router.delete("/{service_id}", response_model=ServiceOut)
def delete_service(service_id: UUID, db: Session = Depends(get_db)):
    svc = crud_service.delete_service(db, service_id)
    if not svc:
        raise HTTPException(status_code=404, detail="Service not found")
    return svc
