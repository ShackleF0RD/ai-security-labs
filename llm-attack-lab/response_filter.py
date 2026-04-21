SENSITIVE_PATTERNS = [
    "system prompt",
    "hidden instructions",
    "confidential",
    "secret",
    "override safeguards",
    "bypass safety"
]


def validate_response(text: str) -> bool:
    lower_text = text.lower()

    for pattern in SENSITIVE_PATTERNS:
        if pattern in lower_text:
            return False

    return True