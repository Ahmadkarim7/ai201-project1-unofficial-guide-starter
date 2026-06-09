# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain
My system focuses on student reviews of college professors. Official college websites provide course descriptions and faculty information, but they do not describe what students actually experience in the classroom. Professor reviews contain valuable information about teaching style, assignment difficulty, workload, feedback quality, and overall student satisfaction. This information is difficult to find through official channels because it comes directly from student experiences rather than institutional sources.

---

## Document Sources

| # | Source |     Type         | URL or file path |
|---|--------|------------------|-----------------|
| 1 | | | |. Local Text File.  | documents/robert_kueper_reviews.txt
| 2 | | | |. Local Text File   | documents/guozhen_an_reviews.txt
| 3 | | | |. Local Text File    |documents/joann_sun_reviews.txt
| 4 | | | |. Local Text File.   |documents/craig_weber_reviews.txt
| 5 | | | |  Local Text File.   |documents/ali_ragoub_reviews.txt
| 6 | | | |  Local Text File.   |documents/emily_epple_reviews.txt
| 7 | | | |  Local Text File.   |documents/danny_mangra_reviews.txt
| 8 | | | |. Local Text File.   |documents/steven_trowbridge_reviews.txt
| 9 | | | |  Local Text File.   |documents/huixin_wu_reviews.txt
| 10 | | | | Local Text File.   |documents/belle_birchfield_reviews.txt

---

## Chunking Strategy

**Chunk size:**
The original design used one review per chunk. After testing retrieval quality, I updated the implementation to combine two reviews into each chunk.
**Overlap:**
No overlap was used because professor metadata was included in every chunk and the reviews were already self-contained.
**Why these choices fit your documents:**
My documents consisted of short professor reviews, usually one or two sentences each. During retrieval testing, single-review chunks were often too small and produced weaker semantic matches. Grouping two reviews together provided more context while still keeping the chunk focused on a single professor.
**Final chunk count:**
80 chunks
---

## Sample Chunks

### Sample Chunk 1
**Source:** robert_kueper_reviews.txt  
**Professor:** Robert Kueper  
**Chunk Index:** 0

Review 1:  
Professor Kueper explains engineering concepts in a way that is easy for beginners to understand.

Review 2:  
The class is organized and expectations are clear from the first day.

---

### Sample Chunk 2
**Source:** craig_weber_reviews.txt  
**Professor:** Craig Weber  
**Chunk Index:** 1

Review 3:  
Projects were interesting and relevant to the field of design.

Review 4:  
Feedback was detailed and helped improve my work.

---

### Sample Chunk 3
**Source:** guozhen_an_reviews.txt  
**Professor:** Guozhen An  
**Chunk Index:** 1

Review 3:  
Assignments were significantly harder than examples shown in class.

Review 4:  
The professor knows the material well but struggles to communicate concepts clearly.

---

### Sample Chunk 4
**Source:** joann_sun_reviews.txt  
**Professor:** Joann Sun  
**Chunk Index:** 5

Review 11:  
I struggled to understand key concepts from lectures alone.

Review 12:  
The class required a lot of independent learning.

---

### Sample Chunk 5
**Source:** emily_epple_reviews.txt  
**Professor:** Emily Epple  
**Chunk Index:** 6

Review 13:  
I learned a lot while still maintaining a reasonable workload.

Review 14:  
I would strongly recommend this professor to other students.

## Embedding Model

**Model used:**
all-MiniLM-L6-v2 from Sentence Transformers
**Production tradeoff reflection:**
I chose all-MiniLM-L6-v2 because it runs locally, is free, and provides strong semantic search performance for small datasets. If I were deploying this system for real users, I would compare larger embedding models that provide better semantic understanding, multilingual support, and improved retrieval accuracy. I would also consider API-hosted embedding models if retrieval quality justified the additional cost.

---

## Grounded Generation

**System prompt grounding instruction:**
The system prompt explicitly instructed the model to answer only from the retrieved documents. The prompt stated: "You must answer using ONLY the retrieved context provided by the system. Do not use outside knowledge. Do not guess. If the context does not contain enough information, say 'I don't have enough information in the provided documents to answer that.'"
This prevents the model from relying on general knowledge outside the review dataset.


**How source attribution is surfaced in the response:**
Retrieved source documents are attached programmatically to every response. The interface displays both the generated answer and the list of retrieved source files used during retrieval.
---

## Evaluation Report

Evaluation Report
| # | Question                                                 | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------------------------------------------------------|-----------------|------------------------------|-------------------|-------------------|
1	Which professor is best for beginners?	                   | Robert Kueper	  |Returned Robert Kueper as strongest match but also included Steven Trowbridge |	Relevant |	Partially Accurate
2	Which professor is the most difficult?	                    |Guozhen An	  |Correctly identified Guozhen An based on difficult assignments and exams |	Relevant	| Accurate
3	Which professor requires the most independent learning?	|Joann Sun	   |    Correctly identified Joann Sun because reviews explicitly mentioned independent learning |	Relevant |	Accurate
4	Which professor gives the most useful feedback?	          |Robert Kueper	  |Correctly identified Robert Kueper based on helpful assignment feedback |	Relevant |	Accurate
5	Which professor is most recommended overall?	               |mily Epple	 |  Correctly identified Emily Epple because reviews strongly recommended her to other students |	Relevant |	Accurate

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

**Question that failed:**
Which professor is best for beginners?
**What the system returned:**
The system correctly identified Robert Kueper but also included Steven Trowbridge as a possible answer.
**Root cause (tied to a specific pipeline stage):**
This was primarily a retrieval-stage issue. Several professors had reviews containing similar language such as "approachable," "organized," and "helpful." Because the embedding model recognized these terms as semantically related, retrieval returned chunks from multiple professors instead of focusing only on Robert Kueper.
**What you would change to fix it:**
I would experiment with larger embedding models, reranking methods, and metadata-based filtering to improve retrieval precision. I would also collect more reviews to create stronger distinctions between professors.
---

## Spec Reflection

**One way the spec helped you during implementation:**
The planning document helped me think about the entire pipeline before writing code. By defining the chunking strategy, retrieval approach, evaluation questions, and anticipated challenges early, I had a clear roadmap during implementation. This reduced confusion and helped me build the project in stages.
**One way your implementation diverged from the spec, and why:**
My original plan was to use one review per chunk. After retrieval testing, I discovered that many chunks were too short and produced weaker semantic matches. I modified the implementation to combine two reviews per chunk because larger chunks provided more context for the embedding model and improved retrieval quality.
---

## AI Usage

**Instance 1**
What I gave the AI: 
 My planning document's chunking strategy and examples of professor review files.
What it produced: 
An ingestion and chunking pipeline that loaded review files and split them into chunks.
What I changed or overrode: 
I changed the chunking implementation from one review per chunk to two reviews per chunk after retrieval testing showed that single-review chunks were too short.

**Instance 2**
What I gave the AI:
 My retrieval architecture, embedding model selection, and ChromaDB requirements.
What it produced:
 Code that generated embeddings, stored them in ChromaDB, and performed semantic retrieval.
What I changed or overrode: 
I manually tested retrieval quality, adjusted evaluation queries, and inspected retrieved chunks to ensure they were actually relevant before moving on to generation.