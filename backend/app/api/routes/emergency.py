from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, Dict
from pydantic import BaseModel
import requests
import traceback
import json

from app.core.config import settings
from app.db.session import get_db
from app.models.ping_log import PingLog
from fastapi.encoders import jsonable_encoder

print("✅ Emergency router loaded")

emergency_router = APIRouter()

EMERGENCY_PINGS = []
LIVE_TRACKING = {}  # device_id -> {timestamp, lat, lon, ip}


class PingPayload(BaseModel):
    screen: Dict[str, int]
    gps: Optional[Dict[str, float]] = None


@emergency_router.post("/ping")
async def send_emergency_ping(payload: PingPayload, request: Request, db: Session = Depends(get_db)):
    ip = request.client.host
    try:
        geo_res = requests.get(f"https://ipinfo.io/{ip}/json?token={settings.IPINFO_TOKEN}")
        geo_data = geo_res.json()

        loc = geo_data.get("loc", "").split(",")
        lat, lon = (float(loc[0]), float(loc[1])) if len(loc) == 2 else (None, None)

        # Ensure gps/screen are dicts, not strings
        gps = payload.gps if isinstance(payload.gps, dict) else json.loads(payload.gps)
        screen = payload.screen if isinstance(payload.screen, dict) else json.loads(payload.screen)

        log = PingLog(
            ip=ip,
            city=geo_data.get("city"),
            region=geo_data.get("region"),
            country=geo_data.get("country"),
            lat=lat,
            lon=lon,
            gps=gps,
            screen=screen,
            org=geo_data.get("org"),
            hostname=geo_data.get("hostname"),
            source="ping"
        )

        db.add(log)
        db.commit()
        db.refresh(log)

        return JSONResponse(content={"success": True, "data": jsonable_encoder(log)})

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})


@emergency_router.get("/locations")
def get_emergency_locations():
    return {"success": True, "data": EMERGENCY_PINGS}


@emergency_router.get("/check-status")
def check_status(device_id: str, timeout_minutes: int = 60):
    tracking = LIVE_TRACKING.get(device_id)

    if not tracking:
        return JSONResponse(content={"success": False, "error": "Device not found"}, status_code=404)

    last_seen = datetime.fromisoformat(tracking["timestamp"])
    inactive_for = datetime.utcnow() - last_seen
    is_active = inactive_for < timedelta(minutes=timeout_minutes)

    return {
        "success": True,
        "device_id": device_id,
        "last_seen": tracking["timestamp"],
        "inactive_for_minutes": round(inactive_for.total_seconds() / 60, 2),
        "status": "active" if is_active else "inactive",
        "location": {
            "lat": tracking["lat"],
            "lon": tracking["lon"],
            "ip": tracking["ip"]
        },
        "alert_recommended": not is_active
    }


@emergency_router.get("/ip-lookup/{ip}")
def ip_lookup(ip: str, db: Session = Depends(get_db)):
    try:
        res = requests.get(f"https://ipinfo.io/{ip}/json?token={settings.IPINFO_TOKEN}")
        if res.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch IP info")

        data = res.json()
        loc = data.get("loc", "").split(",")
        lat, lon = (float(loc[0]), float(loc[1])) if len(loc) == 2 else (None, None)

        log = PingLog(
            ip=data.get("ip"),
            city=data.get("city"),
            region=data.get("region"),
            country=data.get("country"),
            lat=lat,
            lon=lon,
            org=data.get("org"),
            hostname=data.get("hostname"),
            source="manual"
        )

        db.add(log)
        db.commit()

        return {
            "ip": log.ip,
            "city": log.city,
            "region": log.region,
            "country": log.country,
            "lat": log.lat,
            "lon": log.lon,
            "org": log.org,
            "hostname": log.hostname
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"IP lookup failed: {str(e)}")


@emergency_router.get("/all-logs")
def list_all_logs(db: Session = Depends(get_db)):
    logs = db.query(PingLog).order_by(PingLog.created_at.desc()).all()
    return {"data": [log.__dict__ for log in logs]}
