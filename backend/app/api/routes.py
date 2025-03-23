from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
import requests
from urllib.parse import urlparse

router = APIRouter()

@router.get("/scan")
def scan_website(url: str = Query(...)):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; PrivacyAuditBot/1.0)"
        }
        response = requests.get(url, headers=headers, timeout=10)

        cookies = response.cookies.get_dict()
        all_headers = dict(response.headers)

        third_party_domains = []
        parsed_main = urlparse(url).netloc

        for link in response.text.split('"'):
            if link.startswith("http") and parsed_main not in link:
                domain = urlparse(link).netloc
                if domain and domain not in third_party_domains:
                    third_party_domains.append(domain)

        return JSONResponse(content={
            "url": url,
            "status_code": response.status_code,
            "headers": all_headers,
            "cookies": cookies,
            "third_party_domains": third_party_domains,
        })

    except requests.exceptions.RequestException as req_err:
        return JSONResponse(
            content={"error": f"Request failed: {str(req_err)}"}, status_code=500
        )
    except Exception as e:
        return JSONResponse(content={"error": f"Unhandled error: {str(e)}"}, status_code=500)
