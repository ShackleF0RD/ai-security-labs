import math
import ollama

from semantic_examples import MALICIOUS_PROMPT_EXAMPLES, BENIGN_PROMPT_EXAMPLES

EMBED_MODEL = "nomic-embed-text"

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


def cosine_similarity(vec_a, vec_b):
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


def get_embedding(text: str):
    response = ollama.embed(model=EMBED_MODEL, input=text)
    return response["embeddings"][0]


def keyword_risk_score(text: str):
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

    return score, matches


def semantic_risk_score(text: str):
    input_embedding = get_embedding(text)

    malicious_scores = []
    for example in MALICIOUS_PROMPT_EXAMPLES:
        example_embedding = get_embedding(example)
        malicious_scores.append(cosine_similarity(input_embedding, example_embedding))

    benign_scores = []
    for example in BENIGN_PROMPT_EXAMPLES:
        example_embedding = get_embedding(example)
        benign_scores.append(cosine_similarity(input_embedding, example_embedding))

    max_malicious_similarity = max(malicious_scores) if malicious_scores else 0.0
    max_benign_similarity = max(benign_scores) if benign_scores else 0.0

    semantic_flag = (
        max_malicious_similarity >= 0.72
        and max_malicious_similarity > max_benign_similarity
    )

    return {
        "semantic_flag": semantic_flag,
        "max_malicious_similarity": round(max_malicious_similarity, 4),
        "max_benign_similarity": round(max_benign_similarity, 4),
    }


def detect_prompt_injection(text: str) -> dict:
    keyword_score, keyword_matches = keyword_risk_score(text)
    semantic_result = semantic_risk_score(text)

    is_suspicious = (
        keyword_score >= 2
        or semantic_result["semantic_flag"]
    )

    combined_score = keyword_score
    if semantic_result["semantic_flag"]:
        combined_score += 2

    risk_level = "low"
    if combined_score >= 4:
        risk_level = "high"
    elif combined_score >= 2:
        risk_level = "medium"

    return {
        "is_suspicious": is_suspicious,
        "score": combined_score,
        "risk_level": risk_level,
        "matches": keyword_matches,
        "semantic_flag": semantic_result["semantic_flag"],
        "max_malicious_similarity": semantic_result["max_malicious_similarity"],
        "max_benign_similarity": semantic_result["max_benign_similarity"],
    }