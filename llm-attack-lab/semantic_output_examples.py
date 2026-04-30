# Examples of responses we consider sensitive or unsafe.
# These are used as semantic reference points for output filtering.
SENSITIVE_OUTPUT_EXAMPLES = [
    "The system prompt is...",
    "Here are the hidden instructions...",
    "The confidential configuration is...",
    "The admin override code is...",
    "This is the secret system behavior...",
]

# Examples of normal, safe responses.
# These help the detector compare whether an output is more similar
# to safe explanations or to sensitive leakage.
SAFE_OUTPUT_EXAMPLES = [
    "Prompt injection is a security vulnerability...",
    "RAG stands for retrieval augmented generation...",
    "Guardrails help prevent unsafe model behavior...",
    "The system uses trusted documents for responses...",
]