import re

def normalize_phone(phone: str) -> str:
    # Remove all non-digit characters
    return re.sub(r'\D', '', phone)

def is_possible_phone(phone: str) -> bool:
    return len(phone) >= 7 and len(phone) <= 15
