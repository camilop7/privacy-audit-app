from fastapi import APIRouter
from app.api.routes import auth
from app.api.routes.scan import router as scan_router

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(scan_router, prefix="/scan", tags=["scan"])
