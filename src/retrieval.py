from pathlib import Path
import json
import chromadb
from sentence_transformers import SentenceTransformer

CHUNKS_FILE = Path("data/chunks.json")
CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "professor_reviews"


def load_chunks():
    if not CHUNKS_FILE.exists():
        raise FileNotFoundError(
            "data/chunks.json not found. Run python src/ingest.py first."
        )

    with CHUNKS_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_vector_store():
    chunks = load_chunks()

    print(f"Loaded {len(chunks)} chunks.")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.PersistentClient(path=CHROMA_DIR)

    # Delete old collection if it exists, so we rebuild cleanly each time
    existing_collections = [c.name for c in client.list_collections()]
    if COLLECTION_NAME in existing_collections:
        client.delete_collection(COLLECTION_NAME)

    collection = client.create_collection(name=COLLECTION_NAME)

    texts = [chunk["text"] for chunk in chunks]
    ids = [f"{chunk['source']}_{chunk['chunk_index']}" for chunk in chunks]

    metadatas = [
        {
            "source": chunk["source"],
            "professor": chunk["professor"],
            "chunk_index": chunk["chunk_index"],
        }
        for chunk in chunks
    ]

    print("Creating embeddings...")
    embeddings = model.encode(texts).tolist()

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f"Stored {len(texts)} chunks in ChromaDB.")


def retrieve(query, top_k=5):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_collection(name=COLLECTION_NAME)

    query_embedding = model.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    return results


def print_results(query, top_k=5):
    print("\n" + "=" * 80)
    print(f"QUERY: {query}")
    print("=" * 80)

    results = retrieve(query, top_k=top_k)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for i, (doc, meta, distance) in enumerate(zip(documents, metadatas, distances), start=1):
        print(f"\nResult {i}")
        print(f"Source: {meta['source']}")
        print(f"Professor: {meta['professor']}")
        print(f"Chunk Index: {meta['chunk_index']}")
        print(f"Distance: {distance:.4f}")
        print("Text:")
        print(doc)


if __name__ == "__main__":
    build_vector_store()

    test_queries = [
    "Which professor is approachable and helpful for new students?",
    "Which professor has difficult exams and hard assignments?",
    "Which professor gives helpful feedback on assignments?",
    ]

    for question in test_queries:
        print_results(question, top_k=5)