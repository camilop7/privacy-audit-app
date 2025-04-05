from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from worker.tasks import run_phone_scan

phone_router = APIRouter()

@phone_router.get("/scan-phone")
def scan_phone_number(phone: str = Query(..., description="Phone number to scan")):
    try:
        result = run_phone_scan(phone)
        return JSONResponse(content={"success": True, "data": result})
    except Exception as e:
        return JSONResponse(
            content={"success": False, "error": str(e)}, status_code=500
        )
