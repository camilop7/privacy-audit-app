from fastapi import APIRouter

from app.api.routes import auth
from app.api.routes.scan import router as scan_router
from app.api.routes.phone import phone_router
from app.api.routes.emergency import emergency_router
from app.api.routes.admin import admin_router  # ✅ NEW

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(scan_router, prefix="/scan", tags=["scan"])
router.include_router(phone_router, prefix="/phone", tags=["phone"])
router.include_router(emergency_router, prefix="/emergency", tags=["emergency"])
router.include_router(admin_router, prefix="/admin", tags=["admin"])  # ✅ NEW


@router.get("/scan")
def scan_website(url: str = Query(...)):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; PrivacyAuditBot/1.0)"
        }

        is_onion = ".onion" in url
        proxies = {
            "http": "socks5h://127.0.0.1:9050",
            "https": "socks5h://127.0.0.1:9050"
        } if is_onion else None

        response = requests.get(url, headers=headers, timeout=15, proxies=proxies)

        cookies = response.cookies.get_dict()
        all_headers = dict(response.headers)
        parsed_main = urlparse(url).netloc

        third_party_domains = []
        for link in response.text.split('"'):
            if link.startswith("http") and parsed_main not in link:
                domain = urlparse(link).netloc
                if domain and domain not in third_party_domains:
                    third_party_domains.append(domain)

        script_data = analyze_scripts(response.text, parsed_main)
        risk_score, risk_breakdown = script_risk_score(script_data["inline_scripts"])

        return JSONResponse(content={
            "url": url,
            "status_code": response.status_code,
            "headers": all_headers,
            "cookies": cookies,
            "third_party_domains": third_party_domains,
            "script_analysis": script_data,
            "risk_score": risk_score,
            "risk_breakdown": risk_breakdown
        })

    except requests.exceptions.RequestException as req_err:
        return JSONResponse(
            content={"error": f"Request failed: {str(req_err)}"}, status_code=500
        )
    except Exception as e:
        return JSONResponse(content={"error": f"Unhandled error: {str(e)}"}, status_code=500)
