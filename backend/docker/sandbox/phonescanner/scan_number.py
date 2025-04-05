from .phone_utils import normalize_phone, is_possible_phone
from .osint_sources import check_dark_web_sources

def scan_number(phone_number: str) -> dict:
    normalized = normalize_phone(phone_number)

    if not is_possible_phone(normalized):
        raise ValueError("Invalid phone number format")

    dark_web_hits = check_dark_web_sources(normalized)

    return {
        "input": phone_number,
        "normalized": normalized,
        "flags": {
            "dark_web_mentions": len(dark_web_hits),
        },
        "sources": dark_web_hits
    }
