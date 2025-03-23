from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
import requests
from urllib.parse import urlparse
import traceback

from app.services.script_analyzer import analyze_scripts

router = APIRouter()

@router.get("")
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

        # Analyze scripts for potential risks
        script_report = analyze_scripts(response.text)

        return JSONResponse(content={
            "url": url,
            "status_code": response.status_code,
            "headers": all_headers,
            "cookies": cookies,
            "third_party_domains": third_party_domains,
            "script_analysis": script_report
        })

    except requests.exceptions.RequestException as req_err:
        print(f"[Request Error] {req_err}")
        return JSONResponse(
            content={"error": f"Request failed: {str(req_err)}"}, status_code=500
        )
    except Exception as e:
        print(f"[Unhandled Error] {e}")
        traceback.print_exc()
        return JSONResponse(
            content={"error": f"Unhandled error: {str(e)}"}, status_code=500
        )

scan_router = router
