import base64
import io

import pyotp
import qrcode
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_active_user
from app.db.session import get_db
from app.models.user import User

router = APIRouter(prefix="/auth/2fa", tags=["auth"])

APP_ISSUER = "PrivacyApp"

@router.post("/setup")
def setup_2fa(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if current_user.is_2fa_enabled and current_user._totp_secret:
        raise HTTPException(status_code=400, detail="2FA already enabled")

    secret = pyotp.random_base32()
    current_user._totp_secret = secret
    db.add(current_user)
    db.commit()

    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=current_user.email, issuer_name=APP_ISSUER)

    # Generate QR as data URL for easy embedding in front‑end
    img = qrcode.make(uri)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    data_url = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

    return {"otpauth_uri": uri, "qr_data_url": data_url}


@router.post("/enable")
def enable_2fa(code: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if not current_user._totp_secret:
        raise HTTPException(status_code=400, detail="Call /setup first")

    totp = pyotp.TOTP(current_user._totp_secret)
    if not totp.verify(code, valid_window=1):
        raise HTTPException(status_code=400, detail="Invalid code")

    current_user.is_2fa_enabled = True
    db.add(current_user)
    db.commit()
    return {"enabled": True}
