from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
import requests
from datetime import datetime, timedelta
from app.core.config import settings

print("✅ Emergency router loaded")

emergency_router = APIRouter()

# Store emergency pings in memory
EMERGENCY_PINGS = []

@emergency_router.post("/ping")
async def send_emergency_ping(request: Request):
    ip = request.client.host
    try:
        geo_res = requests.get(f"https://ipinfo.io/{ip}/json?token={settings.IPINFO_TOKEN}")
        geo_data = geo_res.json()

        loc_split = geo_data.get("loc", "").split(",")
        lat, lon = (float(loc_split[0]), float(loc_split[1])) if len(loc_split) == 2 else (None, None)

        location_data = {
            "ip": ip,
            "city": geo_data.get("city"),
            "region": geo_data.get("region"),
            "country": geo_data.get("country"),
            "lat": lat,
            "lon": lon,
        }

        EMERGENCY_PINGS.append(location_data)
        return JSONResponse(content={"success": True, "data": location_data})

    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)


@emergency_router.get("/locations")
def get_emergency_locations():
    return {"success": True, "data": EMERGENCY_PINGS}


LIVE_TRACKING = {}  # device_id -> {timestamp, lat, lon, ip}

@emergency_router.post("/live-ping")
async def live_ping(request: Request):
    data = await request.json()
    device_id = data.get("device_id")
    lat = data.get("lat")
    lon = data.get("lon")
    ip = request.client.host

    if not device_id:
        return JSONResponse(content={"success": False, "error": "Missing device_id"}, status_code=400)

    LIVE_TRACKING[device_id] = {
        "timestamp": datetime.utcnow().isoformat(),
        "lat": lat,
        "lon": lon,
        "ip": ip,
    }

    return JSONResponse(content={"success": True, "message": "Ping received"})


@emergency_router.get("/check-status")
def check_status(device_id: str, timeout_minutes: int = 60):
    tracking = LIVE_TRACKING.get(device_id)

    if not tracking:
        return JSONResponse(content={"success": False, "error": "Device not found"}, status_code=404)

    last_seen = datetime.fromisoformat(tracking["timestamp"])
    inactive_for = datetime.utcnow() - last_seen
    is_active = inactive_for < timedelta(minutes=timeout_minutes)

    return JSONResponse(content={
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
    })


# ✅ NEW IP lookup route using IPInfo API
@emergency_router.get("/ip-lookup/{ip}")
def ip_lookup(ip: str):
    try:
        res = requests.get(f"https://ipinfo.io/{ip}/json?token={settings.IPINFO_TOKEN}")
        if res.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch IP info")

        data = res.json()
        loc = data.get("loc", "").split(",")
        lat, lon = (float(loc[0]), float(loc[1])) if len(loc) == 2 else (None, None)

        return {
            "ip": data.get("ip"),
            "city": data.get("city"),
            "region": data.get("region"),
            "country": data.get("country"),
            "lat": lat,
            "lon": lon,
            "org": data.get("org"),
            "hostname": data.get("hostname"),
            "vpn": data.get("privacy", {}).get("vpn") if "privacy" in data else None,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"IP lookup failed: {str(e)}")
