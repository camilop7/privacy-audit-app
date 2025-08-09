from fastapi import APIRouter, Depends
from app.core.security import get_current_active_user
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
def read_me(current_user: User = Depends(get_current_active_user)):
    return {"id": str(current_user.id), "email": current_user.email, "is_2fa_enabled": current_user.is_2fa_enabled}
