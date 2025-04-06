from fastapi import APIRouter

from app.api.routes import auth
from app.api.routes.scan import router as scan_router
from app.api.routes.phone import phone_router
from app.api.routes.emergency import emergency_router
from app.api.routes.admin import admin_router

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(scan_router, prefix="/scan", tags=["scan"])
router.include_router(phone_router, prefix="/phone", tags=["phone"])
router.include_router(emergency_router, prefix="/emergency", tags=["emergency"])
router.include_router(admin_router, prefix="/admin", tags=["admin"])
