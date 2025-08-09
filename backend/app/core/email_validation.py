import re
from typing import Tuple

# RFC5322‑ish but pragmatic; requires a TLD and prevents leading/trailing hyphens
EMAIL_REGEX = re.compile(
    r"^(?=.{1,254}$)(?=.{1,64}@)"  # overall + local length caps
    r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+"  # local part (no spaces, no quotes)
    r"@"
    r"(?:(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+"  # one or more labels
    r"[A-Za-z]{2,63}$"  # TLD
)

DISPOSABLE_DOMAINS = {
    # seed a few; extend from a maintained list
    "mailinator.com", "guerrillamail.com", "10minutemail.com", "yopmail.com",
}


def valid_email_syntax(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email or ""))


def is_disposable(domain: str) -> bool:
    return domain.lower() in DISPOSABLE_DOMAINS

# Optional: MX check using dnspython
try:
    import dns.resolver  # type: ignore
except Exception:  # keep soft‑optional
    dns = None


def has_mx(domain: str) -> Tuple[bool, str]:
    if not dns:
        return False, "dns.resolver not installed"
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        return len(answers) > 0, ""
    except Exception as e:
        return False, str(e)
