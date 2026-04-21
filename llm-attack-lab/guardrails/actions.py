from detector import detect_prompt_injection
from response_filter import validate_response


def check_input_policy(user_text: str):
    detection = detect_prompt_injection(user_text)
    return detection


def check_output_policy(output_text: str):
    return validate_response(output_text)