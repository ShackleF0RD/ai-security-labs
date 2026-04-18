import chromadb
import ollama

CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "secure_rag_docs"
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
    retrieved = retrieve_context(question)

    context_parts = []
    for doc, meta in retrieved:
        context_parts.append(
            f"Source: {meta['source']} | Chunk: {meta['chunk']}\n{doc}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are a secure assistant. Answer only from the provided context.
If the answer is not in the context, say: "I do not know based on the provided documents."

Context:
{context}

Question:
{question}
"""

    response = ollama.chat(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return context, response["message"]["content"]


if __name__ == "__main__":
    user_question = input("Ask a question: ")
    context, answer = answer_question(user_question)

    print("\n--- Retrieved Context ---\n")
    print(context)

    print("\n--- Answer ---\n")
    print(answer)