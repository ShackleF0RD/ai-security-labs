import os
import uuid
import chromadb
import ollama

DATA_DIR = "data"
CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "attack_lab_docs"
EMBED_MODEL = "nomic-embed-text"


RISKY_CONTENT_PATTERNS = [
    "ignore previous instructions",
    "ignore all instructions",
    "reveal system prompt",
    "reveal hidden instructions",
    "bypass safety",
    "override safeguards",
    "confidential",
    "secret",
    "developer mode",
    "act as admin"
]


def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50):
    # Split documents into smaller overlapping chunks.
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


def get_embedding(text: str):
    # Convert text into an embedding vector using Ollama.
    response = ollama.embed(model=EMBED_MODEL, input=text)
    return response["embeddings"][0]


def base_source_score(filename: str):
    # Starting trust score based on source identity.
    # This is source-level trust.
    lower_name = filename.lower()

    if "malicious" in lower_name:
        return 0.2
    elif "trusted" in lower_name:
        return 0.9
    elif "neutral" in lower_name:
        return 0.6
    else:
        return 0.5


def content_risk_score(text: str):
    # Content-level risk analysis.
    # The more suspicious patterns found, the higher the risk.
    lower_text = text.lower()

    matches = [
        pattern for pattern in RISKY_CONTENT_PATTERNS
        if pattern in lower_text
    ]

    risk = min(len(matches) * 0.15, 0.6)

    return {
        "risk": round(risk, 2),
        "matches": matches
    }


def calculate_dynamic_trust_score(filename: str, chunk: str):
    # Combine source trust with content risk.
    source_score = base_source_score(filename)
    risk_result = content_risk_score(chunk)

    # Final trust score decreases as content risk increases.
    final_score = source_score - risk_result["risk"]

    # Keep score between 0.0 and 1.0.
    final_score = max(0.0, min(1.0, final_score))

    return {
        "trust_score": round(final_score, 2),
        "source_score": source_score,
        "content_risk": risk_result["risk"],
        "risk_matches": risk_result["matches"]
    }


def main():
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    for filename in os.listdir(DATA_DIR):
        if not filename.endswith(".txt"):
            continue

        path = os.path.join(DATA_DIR, filename)

        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = chunk_text(text)

        for i, chunk in enumerate(chunks):
            embedding = get_embedding(chunk)
            trust_result = calculate_dynamic_trust_score(filename, chunk)

            collection.add(
                ids=[str(uuid.uuid4())],
                documents=[chunk],
                embeddings=[embedding],
                metadatas=[{
                    "source": filename,
                    "chunk": i,
                    "trust_score": trust_result["trust_score"],
                    "source_score": trust_result["source_score"],
                    "content_risk": trust_result["content_risk"],
                    "risk_matches": str(trust_result["risk_matches"])
                }]
            )

            print(
                f"Ingested {filename} chunk {i} | "
                f"trust_score={trust_result['trust_score']} | "
                f"source_score={trust_result['source_score']} | "
                f"content_risk={trust_result['content_risk']} | "
                f"matches={trust_result['risk_matches']}"
            )

    print("Ingestion complete.")


if __name__ == "__main__":
    main()