from pathlib import Path
import re
import json
import html

DOCUMENTS_DIR = Path("documents")
OUTPUT_DIR = Path("data")
OUTPUT_FILE = OUTPUT_DIR / "chunks.json"


def clean_text(text):
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def load_documents():
    documents = []

    for file_path in DOCUMENTS_DIR.glob("*.txt"):
        raw_text = file_path.read_text(encoding="utf-8")
        cleaned_text = clean_text(raw_text)

        documents.append({
            "source": file_path.name,
            "text": cleaned_text
        })

    return documents


def chunk_by_reviews(document):
    source = document["source"]
    text = document["text"]

    professor_name = source.replace("_reviews.txt", "").replace("_", " ").title()

    review_parts = re.split(r"(Review\s+\d+\s*:?)", text, flags=re.IGNORECASE)

    chunks = []

    if len(review_parts) > 1:
        for i in range(1, len(review_parts), 2):
            review_label = review_parts[i].strip()
            review_text = review_parts[i + 1].strip() if i + 1 < len(review_parts) else ""

            if review_text:
                chunk_text = f"Professor: {professor_name}\nSource: {source}\n{review_label}\n{review_text}"

                chunks.append({
                    "source": source,
                    "professor": professor_name,
                    "chunk_index": len(chunks),
                    "text": chunk_text
                })
    else:
        chunks.append({
            "source": source,
            "professor": professor_name,
            "chunk_index": 0,
            "text": f"Professor: {professor_name}\nSource: {source}\n{text}"
        })

    return chunks


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    documents = load_documents()

    print(f"Loaded {len(documents)} documents.")

    all_chunks = []

    for document in documents:
        chunks = chunk_by_reviews(document)
        all_chunks.extend(chunks)

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print(f"Created {len(all_chunks)} chunks.")
    print(f"Saved chunks to {OUTPUT_FILE}")

    print("\nSample chunks:\n")

    for chunk in all_chunks[:5]:
        print("-" * 60)
        print(f"Source: {chunk['source']}")
        print(f"Professor: {chunk['professor']}")
        print(chunk["text"][:700])


if __name__ == "__main__":
    main()