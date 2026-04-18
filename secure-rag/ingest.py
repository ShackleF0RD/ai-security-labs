import os
import uuid
import chromadb
import ollama

DATA_DIR = "data"
CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "secure_rag_docs"
EMBED_MODEL = "nomic-embed-text"


def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def get_embedding(text: str):
    response = ollama.embed(model=EMBED_MODEL, input=text)
    return response["embeddings"][0]


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
            collection.add(
                ids=[str(uuid.uuid4())],
                documents=[chunk],
                embeddings=[embedding],
                metadatas=[{"source": filename, "chunk": i}]
            )

        print(f"Ingested {filename} with {len(chunks)} chunks.")

    print("Ingestion complete.")


if __name__ == "__main__":
    main()