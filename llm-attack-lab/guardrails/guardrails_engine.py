from detector import detect_prompt_injection
from response_filter import semantic_output_check
from logger import log_event


def apply_input_guardrails(user_text: str):
    # Run prompt injection detection on the user's input.
    detection = detect_prompt_injection(user_text)

    # Log detection details for dashboard and audit trail.
    log_event(
        "guardrail_input_check",
        {
            "question": user_text,
            "detection": detection
        }
    )

    # IMPORTANT:
    # The returned message must start with "Blocked:"
    # because auto_attack.py uses result.startswith("Blocked:")
    # to count blocked attacks correctly.
    if detection["is_suspicious"]:
        return False, (
            f"Blocked: suspicious prompt detected by policy engine. "
            f"Risk={detection['risk_level']}, "
            f"Score={detection['score']}, "
            f"Matches={detection['matches']}"
        )

    return True, None


def apply_output_guardrails(question: str, output_text: str):
    # Run semantic output detection on the model response.
    result = semantic_output_check(output_text)

    # Log semantic output safety details.
    log_event(
        "guardrail_output_check",
        {
            "question": question,
            "output_safe": not result["is_sensitive"],
            "max_sensitive_similarity": result["max_sensitive_similarity"],
            "max_safe_similarity": result["max_safe_similarity"],
        }
    )

    # IMPORTANT:
    # This also starts with "Blocked:" so automated tests count it properly.
    if result["is_sensitive"]:
        return False, "Blocked: unsafe response detected by policy engine."

    return True, None