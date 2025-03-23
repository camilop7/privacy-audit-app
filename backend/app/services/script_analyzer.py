from bs4 import BeautifulSoup
import re
import base64

def analyze_scripts(html_content: str) -> dict:
    soup = BeautifulSoup(html_content, "html.parser")
    scripts = soup.find_all("script")

    inline_scripts = []
    external_scripts = []

    for script in scripts:
        src = script.get("src")
        if src:
            external_scripts.append({"src": src, "is_third_party": is_third_party(src)})
        else:
            content = script.string or ""
            inline_scripts.append({"length": len(content), "preview": content.strip()[:300]})

    risk_score, breakdown = script_risk_score(inline_scripts)

    return {
        "external_scripts": external_scripts,
        "inline_scripts": inline_scripts,
        "total_scripts": len(scripts),
        "risk_score": risk_score,
        "risk_breakdown": breakdown
    }

def is_third_party(src: str) -> bool:
    return src.startswith("http") or src.startswith("//")

def script_risk_score(inline_scripts: list) -> (int, dict):
    score = 0
    breakdown = {
        "eval_detected": 0,
        "document_write_detected": 0,
        "function_constructor_detected": 0,
        "base64_detected": 0,
        "obfuscated_detected": 0,
        "minified_detected": 0,
    }

    for script in inline_scripts:
        content = script.get("preview", "")

        if "eval(" in content:
            score += 10
            breakdown["eval_detected"] += 1
        if "document.write" in content:
            score += 5
            breakdown["document_write_detected"] += 1
        if "Function(" in content:
            score += 10
            breakdown["function_constructor_detected"] += 1
        if "atob(" in content or "btoa(" in content:
            score += 5
            breakdown["base64_detected"] += 1
        if re.search(r"\\x[0-9a-fA-F]{2}", content) or re.search(r"\\u[0-9a-fA-F]{4}", content):
            score += 8
            breakdown["obfuscated_detected"] += 1
        if len(content) > 500 and content.count(";") > 50:
            score += 3
            breakdown["minified_detected"] += 1

    score = min(score, 100)
    return score, breakdown
