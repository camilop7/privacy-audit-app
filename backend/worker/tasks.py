import os
import requests

NUMVERIFY_API_KEY = os.getenv("NUMVERIFY_API_KEY")
NUMVERIFY_BASE_URL = "http://apilayer.net/api/validate"

def run_phone_scan(phone: str) -> dict:
    params = {
        "access_key": NUMVERIFY_API_KEY,
        "number": phone,
        "format": 1
    }

    try:
        response = requests.get(NUMVERIFY_BASE_URL, params=params, timeout=10)
        data = response.json()

        if not data.get("valid"):
            return {
                "phone": phone,
                "valid": False,
                "risk_score": 80,  # Consider invalid = higher risk
                "fraud_likelihood": "High",
                "blacklist_match": False,
                "notes": ["Number is not valid."],
            }

        risk_score = 10  # Low risk by default
        notes = []

        if data.get("line_type") == "voip":
            risk_score += 25
            notes.append("Number is VOIP — often used in scams.")
        if not data.get("location"):
            risk_score += 15
            notes.append("No location data found.")
        if not data.get("carrier"):
            risk_score += 15
            notes.append("Unknown carrier — potentially burner phone.")

        fraud_likelihood = (
            "Low" if risk_score < 25 else
            "Medium" if risk_score < 60 else
            "High"
        )

        return {
            "phone": phone,
            "valid": True,
            "risk_score": risk_score,
            "fraud_likelihood": fraud_likelihood,
            "blacklist_match": False,  # Placeholder until we add blacklists
            "carrier": data.get("carrier", "Unknown"),
            "country": data.get("country_name", "Unknown"),
            "line_type": data.get("line_type", "Unknown"),
            "notes": notes or ["No suspicious flags detected."]
        }

    except Exception as e:
        return {
            "phone": phone,
            "valid": False,
            "error": str(e),
            "risk_score": 50,
            "fraud_likelihood": "Unknown",
            "blacklist_match": False,
            "notes": ["Failed to complete lookup."]
        }
