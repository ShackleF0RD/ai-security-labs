import chromadb
import ollama
from detector import detect_prompt_injection
from logger import log_event

CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "attack_lab_docs"
EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL = "qwen3:4b"

def get_embedding(text: str):
    response = ollama.embed(model=EMBED_MODEL, input=text)
    return response["embeddings"][0]

def retrieve_context(question: str, n_results: int = 3):
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_collection(name=COLLECTION_NAME)

    query_embedding = get_embedding(question)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas"]
    )

    docs = results["documents"][0]
    metas = results["metadatas"][0]
    return list(zip(docs, metas))

def answer_question(question: str):
    detection = detect_prompt_injection(question)
    log_event("prompt_check", {"question": question, "detection": detection})

    if detection["is_suspicious"]:
        return "Blocked: suspicious prompt detected."

    retrieved = retrieve_context(question)

    filtered = [(doc, meta) for doc, meta in retrieved if meta.get("trust_level") == "trusted"]

    if not filtered:
        return "No trusted context found."

    context_parts = []
    for doc, meta in filtered:
        context_parts.append(f"Source: {meta['source']} | Chunk: {meta['chunk']}\n{doc}")

    context = "\n\n".join(context_parts)

    prompt = f"""
You are a secure assistant. Answer only from the provided trusted context.
If the answer is not in the context, say: "I do not know based on the trusted documents."

Context:
{context}

Question:
{question}
"""

    response = ollama.chat(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    log_event("answer_generated", {
        "question": question,
        "sources": [meta["source"] for _, meta in filtered]
    })

    return response["message"]["content"]

if __name__ == "__main__":
    while True:
        user_question = input("\nAsk a question (or type exit): ")
        if user_question.lower() == "exit":
            break

        answer = answer_question(user_question)
        print("\n--- Answer ---\n")
        print(answer)