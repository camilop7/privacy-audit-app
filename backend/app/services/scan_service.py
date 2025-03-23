import requests
from urllib.parse import urlparse
from app.utils.script_analyzer import analyze_scripts
from bs4 import BeautifulSoup


def perform_scan(url: str) -> dict:
    headers = {
        "User-Agent": "PrivacyAuditBot/1.0"
    }

    is_onion = ".onion" in url
    proxies = {
        "http": "socks5h://127.0.0.1:9050",
        "https": "socks5h://127.0.0.1:9050"
    } if is_onion else None

    try:
        response = requests.get(url, headers=headers, timeout=15, proxies=proxies)
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}

    soup = BeautifulSoup(response.text, "html.parser")

    external_scripts = [
        {"src": tag.get("src"), "is_third_party": is_third_party(tag.get("src"), url)}
        for tag in soup.find_all("script", src=True)
    ]

    inline_scripts = [
        {"length": len(tag.string or ""), "preview": (tag.string or "")[:300]}
        for tag in soup.find_all("script") if not tag.get("src")
    ]

    analysis_result = analyze_scripts(inline_scripts)
    third_party_domains = list({
        get_domain(script["src"]) for script in external_scripts
        if script["src"] and is_third_party(script["src"], url)
    })

    return {
        "url": url,
        "status_code": response.status_code,
        "headers": dict(response.headers),
        "cookies": requests.utils.dict_from_cookiejar(response.cookies),
        "third_party_domains": third_party_domains,
        "script_analysis": {
            "external_scripts": external_scripts,
            "inline_scripts": inline_scripts,
            "total_scripts": len(external_scripts) + len(inline_scripts)
        },
        **analysis_result
    }


def get_domain(script_url):
    try:
        return urlparse(script_url).netloc
    except:
        return ""


def is_third_party(script_url, page_url):
    if not script_url:
        return False
    return urlparse(script_url).netloc not in urlparse(page_url).netloc
