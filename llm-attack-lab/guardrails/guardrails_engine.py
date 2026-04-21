from detector import detect_prompt_injection
from response_filter import validate_response
from logger import log_event


def apply_input_guardrails(user_text: str):
    detection = detect_prompt_injection(user_text)

    log_event(
        "guardrail_input_check",
        {
            "question": user_text,
            "detection": detection
        }
    )

    if detection["is_suspicious"]:
        return False, (
            f"Blocked by policy engine. "
            f"Risk={detection['risk_level']}, Matches={detection['matches']}"
        )

    return True, None


def apply_output_guardrails(question: str, output_text: str):
    is_safe = validate_response(output_text)

    log_event(
        "guardrail_output_check",
        {
            "question": question,
            "output_safe": is_safe,
            "output_preview": output_text[:200]
        }
    )

    if not is_safe:
        return False, "Blocked by policy engine: unsafe output detected."

    return True, None