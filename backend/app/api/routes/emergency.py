from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import requests
from datetime import datetime, timedelta

print("✅ Emergency router loaded")


emergency_router = APIRouter()

# Store emergency pings in memory (can later connect to DB)
EMERGENCY_PINGS = []

@emergency_router.post("/ping")
async def send_emergency_ping(request: Request):
    ip = request.client.host
    try:
        geo_res = requests.get(f"http://ip-api.com/json/{ip}")
        geo_data = geo_res.json()

        location_data = {
            "ip": ip,
            "city": geo_data.get("city"),
            "region": geo_data.get("regionName"),
            "country": geo_data.get("country"),
            "lat": geo_data.get("lat"),
            "lon": geo_data.get("lon"),
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
