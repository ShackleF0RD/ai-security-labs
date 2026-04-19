SUSPICIOUS_PATTERNS = [
    "ignore previous instructions",
    "disregard prior rules",
    "reveal system prompt",
    "reveal hidden instructions",
    "hidden system prompts",
    "bypass safety",
    "override safeguards",
    "developer mode",
    "act as admin",
    "ignore all previous instructions",
    "repeat the system prompt"
]

HIGH_RISK_KEYWORDS = [
    "confidential",
    "hidden",
    "secret",
    "system prompt",
    "override",
    "bypass",
    "admin"
]


def detect_prompt_injection(text: str) -> dict:
    lower_text = text.lower()

    matches = []
    score = 0

    for pattern in SUSPICIOUS_PATTERNS:
        if pattern in lower_text:
            matches.append(pattern)
            score += 2

    for keyword in HIGH_RISK_KEYWORDS:
        if keyword in lower_text and keyword not in matches:
            matches.append(keyword)
            score += 1

    is_suspicious = score >= 2

    risk_level = "low"
    if score >= 4:
        risk_level = "high"
    elif score >= 2:
        risk_level = "medium"

    return {
        "is_suspicious": is_suspicious,
        "score": score,
        "risk_level": risk_level,
        "matches": matches
    }