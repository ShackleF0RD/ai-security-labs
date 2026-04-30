import math
import ollama

# Import semantic reference examples for output filtering.
from semantic_output_examples import SENSITIVE_OUTPUT_EXAMPLES, SAFE_OUTPUT_EXAMPLES

# Embedding model used for semantic comparison.
EMBED_MODEL = "nomic-embed-text"


def cosine_similarity(vec_a, vec_b):
    # Compute similarity between two vectors.
    # Higher similarity means the texts are more alike in meaning.
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


def get_embedding(text: str):
    # Convert text into an embedding vector using Ollama.
    response = ollama.embed(model=EMBED_MODEL, input=text)
    return response["embeddings"][0]


def semantic_output_check(text: str):
    # Create an embedding for the model output we want to evaluate.
    input_embedding = get_embedding(text)

    # Compare output against known sensitive examples.
    sensitive_scores = [
        cosine_similarity(input_embedding, get_embedding(example))
        for example in SENSITIVE_OUTPUT_EXAMPLES
    ]

    # Compare output against known safe examples.
    safe_scores = [
        cosine_similarity(input_embedding, get_embedding(example))
        for example in SAFE_OUTPUT_EXAMPLES
    ]

    # Keep the highest similarity scores from each group.
    max_sensitive = max(sensitive_scores) if sensitive_scores else 0
    max_safe = max(safe_scores) if safe_scores else 0

    # Flag as sensitive if it is more similar to sensitive examples
    # and crosses the chosen threshold.
    is_sensitive = max_sensitive >= 0.70 and max_sensitive > max_safe

    return {
        "is_sensitive": is_sensitive,
        "max_sensitive_similarity": round(max_sensitive, 4),
        "max_safe_similarity": round(max_safe, 4),
    }


def validate_response(text: str):
    # Wrapper used by the rest of the project.
    # Returns True only if the response is considered safe.
    result = semantic_output_check(text)
    return result["is_sensitive"] is False