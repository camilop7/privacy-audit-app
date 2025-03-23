import re
import base64


def analyze_scripts(inline_scripts: list) -> dict:
    eval_count = 0
    document_write_count = 0
    function_constructor_count = 0
    base64_count = 0
    obfuscated_count = 0
    minified_count = 0

    for script in inline_scripts:
        content = script.get("preview", "")

        if "eval(" in content:
            eval_count += 1
        if "document.write(" in content:
            document_write_count += 1
        if "Function(" in content:
            function_constructor_count += 1
        if re.search(r'(atob\(|btoa\()', content):
            base64_count += 1
        if re.search(r'\\x[a-fA-F0-9]{2}', content):
            obfuscated_count += 1
        if len(re.findall(r';', content)) > 50:
            minified_count += 1

    risk_score = (
        eval_count * 5 +
        document_write_count * 4 +
        function_constructor_count * 4 +
        base64_count * 2 +
        obfuscated_count * 5 +
        minified_count * 2
    )

    return {
        "risk_score": min(risk_score, 100),
        "risk_breakdown": {
            "eval_detected": eval_count,
            "document_write_detected": document_write_count,
            "function_constructor_detected": function_constructor_count,
            "base64_detected": base64_count,
            "obfuscated_detected": obfuscated_count,
            "minified_detected": minified_count,
        }
    }
