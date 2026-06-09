import os
from dotenv import load_dotenv
from groq import Groq

from retrieval import retrieve

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def format_context(results):
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    context_blocks = []
    sources = []

    for i, (doc, meta, distance) in enumerate(zip(documents, metadatas, distances), start=1):
        source_label = f"{meta['professor']} ({meta['source']}, chunk {meta['chunk_index']})"
        sources.append(source_label)

        context_blocks.append(
            f"[Source {i}: {source_label}, distance={distance:.4f}]\n{doc}"
        )

    return "\n\n".join(context_blocks), sources


def ask(question, top_k=5):
    results = retrieve(question, top_k=top_k)
    context, sources = format_context(results)

    system_prompt = """
You are an assistant for a RAG system called The Unofficial Guide.

You must answer using ONLY the retrieved context provided by the system.
Do not use outside knowledge.
Do not guess.
If the context does not contain enough information, say:
"I don't have enough information in the provided documents to answer that."

Every answer must mention the source document names used.
Keep the answer clear and concise.
"""

    user_prompt = f"""
Retrieved context:
{context}

User question:
{question}

Answer using only the retrieved context.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "sources": sources,
        "context": context,
    }


if __name__ == "__main__":
    test_questions = [
        "Which professor gives helpful feedback on assignments?",
        "Which professor has difficult exams and hard assignments?",
        "Which professor teaches biology?",
    ]

    for q in test_questions:
        print("\n" + "=" * 80)
        print(f"QUESTION: {q}")
        result = ask(q)
        print("\nANSWER:")
        print(result["answer"])
        print("\nSOURCES:")
        for source in result["sources"]:
            print(f"- {source}")