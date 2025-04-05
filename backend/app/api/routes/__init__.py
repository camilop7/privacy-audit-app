from fastapi import APIRouter
from app.api.routes import auth
from app.api.routes.scan import router as scan_router
from app.api.routes.phone import phone_router

router = APIRouter()

# Existing routes
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(scan_router, prefix="/scan", tags=["scan"])

# New route for phone scanning
router.include_router(phone_router, prefix="/phone", tags=["phone"])  # ✅ NEW
