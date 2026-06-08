# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
This project focuses on student reviews of professors at DePauw University collected from Rate My Professors.

This information is valuable because students often want to know about teaching style, exam difficulty, workload, grading fairness, and responsiveness before choosing a course. Official university websites provide course descriptions and faculty information, but they do not include student experiences and opinions.
---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Rate My Professors | Dave Berque reviews | documents/dave_berque.txt |
| 2 | Rate My Professors | Brian Howard reviews | documents/brian_howard.txt |
| 3 | Rate My Professors | Guangjun Qu reviews | documents/guangjun_qu.txt |
| 4 | Rate My Professors | Tamara Stasik reviews | documents/tamara_stasik.txt |
| 5 | Rate My Professors | Ophelia Goma reviews | documents/ophelia_goma.txt |
| 6 | Rate My Professors | Harry Brown reviews | documents/harry_brown.txt |
| 7 | Rate My Professors | Melanie Finney reviews | documents/melanie_finney.txt |
| 8 | Rate My Professors | Andrea Sununu reviews | documents/andrea_sununu.txt |
| 9 | Rate My Professors | Chris White reviews | documents/chris_white.txt |
| 10 | Rate My Professors | Ron Dye reviews | documents/ron_dye.txt |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 300 characters

**Overlap:** 50 characters

**Reasoning:**

Professor reviews are typically short and opinion-based. A chunk size of 300 characters keeps related comments together while remaining specific enough for retrieval. A 50-character overlap helps preserve context when important information appears near chunk boundaries.

---

## Retrieval Approach


**Embedding model:** all-MiniLM-L6-v2

**Top-k:**
5

**Production tradeoff reflection:**
The all-MiniLM-L6-v2 model was chosen because it runs locally, is free, and performs well on semantic similarity tasks. For a production system, I would consider larger embedding models that provide higher accuracy, support multiple languages, and handle domain-specific terminology better, although they may require more computation and increase latency.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Which professor is considered easiest according to student reviews? | easiest according to student reviews?
The professor with the most positive comments about easy exams and manageable workload. |
| 2 | Which professor provides the most useful feedback? | The professor whose reviews frequently mention detailed feedback and helpful office hours. |
| 3 | Which professor has the most challenging exams? | The professor whose reviews consistently describe exams as difficult. |
| 4 | Which professor is best for beginners? | The professor whose reviews mention patience, clarity, and beginner-friendly teaching. |
| 5 | Which professor is hardest to contact outside class? | The professor whose reviews mention slow responses or lack of availability. |

---

## Anticipated Challenges

1. Reviews may contain inconsistent language and opinions, making retrieval difficult when students describe similar experiences differently.

2. Important information may be split across chunk boundaries, causing retrieval to miss relevant context.

3. Some reviews may be very short and provide limited information for semantic search.

4. The LLM may attempt to answer using prior knowledge instead of only the retrieved reviews if grounding is not enforced correctly.

---

## Architecture

Documents (.txt files)
          |
          v
Document Ingestion (Python)
          |
          v
Chunking (300 chars, 50 overlap)
          |
          v
Embeddings (all-MiniLM-L6-v2)
          |
          v
ChromaDB Vector Store
          |
          v
Retrieval (Top 5 Chunks)
          |
          v
Groq Llama 3.3 70B
          |
          v
Answer + Source Attribution

---

## AI Tool Plan

**Milestone 3 — Ingestion and chunking:**

I will use ChatGPT to help implement document loading and chunking. I will provide the Documents section, Chunking Strategy section, and Architecture diagram. I expect Python code that loads text files from the documents folder and produces chunks with the specified size and overlap. I will verify the output by printing sample chunks.

**Milestone 4 — Embedding and retrieval:**

I will use ChatGPT to help implement embeddings with sentence-transformers and storage in ChromaDB. I will provide the Retrieval Approach section and Architecture diagram. I expect code that embeds chunks, stores metadata, and retrieves top-k relevant chunks. I will verify results using test queries.

**Milestone 5 — Generation and interface:**

I will use ChatGPT to help connect Groq's Llama 3.3 model and create a Gradio interface. I will provide the grounding requirements and output format. I expect code that answers questions using only retrieved context and displays source attribution. I will verify responses against retrieved chunks and test out-of-scope questions.
