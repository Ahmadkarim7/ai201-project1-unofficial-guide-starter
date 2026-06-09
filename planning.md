## Evaluation Plan

### Question 1
Which professor is best for beginners?

Expected Answer:
Robert M. Kueper or Belle Birchfield

### Question 2
Which professor is the most difficult?

Expected Answer:
Joann Sun

### Question 3
Which professor requires the most independent learning?

Expected Answer:
Guozhen An or Joann Sun

### Question 4
Which professor gives the most useful feedback?

Expected Answer:
Craig Weber

### Question 5
Which professor is most recommended overall?

Expected Answer:
Robert M. Kueper, Belle Birchfield, or Ali Ragoub


## Chunking Strategy

My documents are short professor-review files. Each document contains one professor and 15 short reviews. Most reviews are 1–2 sentences long and each review usually focuses on one clear idea, such as teaching style, workload, exams, difficulty, feedback, or support.

Because the reviews are already separated by “Review 1,” “Review 2,” etc., I will chunk by individual review instead of splitting every fixed number of characters. Each chunk will include the professor name, department, rating, difficulty, and one review. This makes each chunk small but still meaningful on its own.

I do not need a large overlap because each review is already self-contained. If needed, I may use a very small overlap by repeating professor metadata in every chunk so the system always knows which professor the review belongs to.

After testing retrieval in Milestone 4, I found that one-review chunks were sometimes too short and produced high distance scores. I updated the chunking strategy to group two reviews per chunk so each chunk has more semantic context while still staying focused on one professor.

## Retrieval Approach

I will use the all-MiniLM-L6-v2 embedding model from sentence-transformers because it runs locally, is free, and is good enough for a small professor-review dataset. I will store embeddings in ChromaDB.

For each user question, I will retrieve the top 4 or 5 most relevant chunks. This should give the LLM enough context from multiple reviews without adding too much unrelated text.

If this were a production system, I would compare embedding models based on accuracy, speed, cost, context length, and whether they handle student-style informal language well.

## Domain

My project focuses on student reviews of professors at Queensborough Community College. Students often want information about teaching style, workload, exam difficulty, grading policies, and classroom experience, but official college websites do not provide this information. This project makes student experiences searchable through a RAG system so students can make better decisions when selecting professors.

## Documents

I collected 10 professor review documents:

- ali_ragoub_reviews.txt
- belle_birchfield_reviews.txt
- craig_weber_reviews.txt
- danny_mangra_reviews.txt
- emily_epple_reviews.txt
- guozhen_an_reviews.txt
- huixin_wu_reviews.txt
- joann_sun_reviews.txt
- robert_kueper_reviews.txt
- steven_trowbridge_reviews.txt

Each file contains approximately 15 student reviews gathered from professor-review sources. Together they cover different teaching styles, workloads, difficulty levels, grading approaches, and student experiences.


## Anticipated Challenges

One challenge is that student reviews are subjective and sometimes contradictory. One student may describe a professor as easy while another describes the same professor as difficult.

Another challenge is retrieval accuracy. Because reviews are short, the system may retrieve reviews that contain similar words but do not actually answer the user's question.

A third challenge is source attribution. Every generated answer must clearly identify which professor-review documents were used to produce the answer.

During Milestone 4 testing, some retrieval distances were high because the review text used general words like "approachable," "helpful," or "challenging" instead of directly matching question terms like "beginner," "feedback," or "difficult." This may cause semantic retrieval to return partially relevant chunks.

During retrieval testing, the system returned relevant chunks, but the distance scores were higher than ideal. This likely happened because the reviews are short and sometimes use broad words like "helpful," "approachable," and "challenging." I adjusted the test queries to better match the language used in the review documents, which improved relevance even though the scores remained somewhat high.
## AI Tool Plan

I will use ChatGPT/Claud to help implement specific parts of the RAG pipeline.

For document ingestion and chunking, I will provide my chunking strategy and ask ChatGPT to help create a script that loads review files and converts them into chunks.

For embeddings and retrieval, I will provide my retrieval approach and ask ChatGPT to help implement all-MiniLM-L6-v2 embeddings and ChromaDB storage.

For generation, I will ask ChatGPT to help create prompts that ensure answers are grounded only in retrieved reviews and include source attribution.

I will review, test, and modify all generated code before using it.


## Architecture

```mermaid
flowchart TD
    A[Professor Review Text Files] --> B[Document Ingestion]
    B --> C[Cleaning and Preprocessing]
    C --> D[Chunking by Individual Review]
    D --> E[Embedding Model: all-MiniLM-L6-v2]
    E --> F[Vector Store: ChromaDB]
    G[User Question] --> H[Semantic Retrieval: Top 4-5 Chunks]
    F --> H
    H --> I[LLM: Groq Llama 3.3 70B Versatile]
    I --> J[Grounded Answer with Source Citations]