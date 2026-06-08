# The Unofficial Guide — Project 1

## Domain

This project focuses on student reviews of professors at DePauw University collected from Rate My Professors.

This knowledge is valuable because students often want information about teaching style, workload, grading fairness, exam difficulty, responsiveness, and overall classroom experience before registering for courses. Official university resources provide course descriptions and faculty information but do not include student perspectives. This RAG system makes professor reviews searchable and answerable through natural language questions.

---

## Document Sources

| #  | Source                 | Type               | URL or File Path             |
| -- | ---------------------- | ------------------ | ---------------------------- |
| 1  | Andrea Sununu Reviews  | Rate My Professors | https://www.ratemyprofessors.com/professor/612108    |
| 2  | Brian Howard Reviews   | Rate My Professors | https://www.ratemyprofessors.com/professor/227705    |
| 3  | Chris White Reviews    | Rate My Professors | https://www.ratemyprofessors.com/professor/659436    |
| 4  | Dave Berque Reviews    | Rate My Professors | https://www.ratemyprofessors.com/professor/18270    |
| 5  | Guangjun Qu Reviews    | Rate My Professors | https://www.ratemyprofessors.com/professor/1483070    |
| 6  | Harry Brown Reviews    | Rate My Professors | https://www.ratemyprofessors.com/professor/695924    |
| 7  | Melanie Finney Reviews | Rate My Professors | https://www.ratemyprofessors.com/professor/680021 |
| 8  | Ophelia Goma Reviews   | Rate My Professors | https://www.ratemyprofessors.com/professor/916240   |
| 9  | Ron Dye Reviews        | Rate My Professors | https://www.ratemyprofessors.com/professor/595062        |
| 10 | Tamara Stasik Reviews  | Rate My Professors | https://www.ratemyprofessors.com/professor/1841545    |

---

## Chunking Strategy

**Chunk size:** Initially 300 characters

**Overlap:** Initially 50 characters

**Why these choices fit the documents:**

The project uses professor reviews, which are short opinion-based documents. I initially used fixed-size character chunking with overlap to preserve context. After testing, I found that this approach frequently split reviews in the middle of words and sentences, reducing retrieval quality.

I switched to paragraph-based chunking because each review naturally represents a complete thought. This preserved context and improved semantic retrieval performance.

**Final chunk count:** 95 chunks across 10 documents

### Sample Chunks

**Source:** brian_howard.txt

> I can say that Professor Howard is the best professor I have at DePauw. He is dedicated. He even writes a book for his students. Very detailed. Gives good feedback. Quizzes and exams are not difficult at all.

**Source:** dave_berque.txt

> Berque is a stand up professor. I've taken multiple courses with him and been thoroughly impressed. He's extremely timely with replying outside of class time and very helpful with providing additional feedback.

**Source:** harry_brown.txt

> Absolutely fantastic professor. Very helpful outside of class. Projects are designed with other classes in mind. Strongly recommended.

**Source:** ron_dye.txt

> Totally laid back professor. Awesome help during office hours. I'd recommend taking one of his classes.

**Source:** guangjun_qu.txt

> Very hard professor who needs everything done exactly as he likes. Very tough grader and difficult exams.

---

## Embedding Model

**Model Used:** all-MiniLM-L6-v2 (Sentence Transformers)

I selected all-MiniLM-L6-v2 because it runs locally, requires no API key, and provides strong semantic retrieval performance for short text documents.

### Production Tradeoff Reflection

If cost were not a constraint, I would consider larger embedding models that provide better retrieval accuracy, stronger multilingual support, and improved understanding of domain-specific language. The tradeoff would be higher latency, greater computational requirements, and potentially higher operating costs.

---

## Retrieval Test Results

### Query 1

**Question:** Which professor provides useful feedback?

**Top Retrieved Sources:**

* brian_howard.txt
* harry_brown.txt
* guangjun_qu.txt

**Why Retrieval Was Relevant:**

The retrieved chunks contained explicit references to feedback quality and helpfulness. Brian Howard's reviews specifically mentioned "good feedback," making retrieval highly relevant.

### Query 2

**Question:** Which professor has difficult exams?

**Top Retrieved Sources:**

* guangjun_qu.txt
* ophelia_goma.txt

**Why Retrieval Was Relevant:**

Retrieved reviews directly discussed exam difficulty and grading standards. Guangjun Qu's reviews frequently described challenging coursework and strict grading.

### Query 3

**Question:** Which professor is most helpful outside class?

**Top Retrieved Sources:**

* harry_brown.txt
* dave_berque.txt
* ron_dye.txt

**Why Retrieval Was Relevant:**

Retrieved chunks contained references to office hours, responsiveness, and willingness to help students outside class.

---

## Grounded Generation

### System Prompt Grounding Instruction

The model was instructed:

> "Answer the question using ONLY the provided context. If the answer is not in the context, say 'I don't have enough information to answer.'"

The retrieved chunks are passed directly to the model as context, preventing it from relying on outside knowledge.

### Source Attribution

Source filenames are stored as metadata in ChromaDB. After generating a response, the application displays all retrieved source files used to answer the question.

---

## Example Responses

### Example 1

**Question:** Which professor provides useful feedback?

**Answer:**

The system identified Brian Howard because multiple reviews described him as providing clear grading criteria and useful feedback.

**Sources:**

* brian_howard.txt
* harry_brown.txt
* guangjun_qu.txt

### Example 2

**Question:** Which professor has the most challenging exams?

**Answer:**

The system identified Guangjun Qu because reviews described his courses as difficult and noted strict grading standards.

**Sources:**

* guangjun_qu.txt
* ophelia_goma.txt

### Out-of-Scope Example

**Question:** Which professor teaches the most sections each semester?

**Answer:**

"I don't have enough information to answer."

This information was not available in the review documents.

---

## Query Interface

The project uses a Gradio web interface.

### Input

A natural-language question about professor reviews.

### Output

* Generated answer
* Retrieved source documents

### Example Interaction

**User:**

Which professor provides useful feedback?

**System:**

Brian Howard appears to provide the most useful feedback because reviews explicitly mention his clear grading criteria and good feedback.

**Sources:**

* brian_howard.txt
* harry_brown.txt

---

## Evaluation Report

| # | Question                                                            | Expected Answer                          | System Response (Summarized)                                        | Retrieval Quality  | Response Accuracy  |
| - | ------------------------------------------------------------------- | ---------------------------------------- | ------------------------------------------------------------------- | ------------------ | ------------------ |
| 1 | Which professor is considered easiest according to student reviews? | Ron Dye                                  | Identified Ron Dye based on lenient grading comments                | Relevant           | Accurate           |
| 2 | Which professor provides the most useful feedback?                  | Brian Howard                             | Identified Brian Howard due to explicit feedback references         | Relevant           | Accurate           |
| 3 | Which professor has the most challenging exams?                     | Guangjun Qu                              | Identified Guangjun Qu as having difficult exams and strict grading | Relevant           | Partially Accurate |
| 4 | Which professor is best for beginners?                              | Professor described as beginner-friendly | System responded that insufficient information was available        | Partially Relevant | Accurate           |
| 5 | Which professor is hardest to contact outside class?                | Professor described as unavailable       | System responded that insufficient information was available        | Partially Relevant | Accurate           |

---

## Failure Case Analysis

### Question That Failed

Which professor is best for beginners?

### What the System Returned

"I don't have enough information to answer."

### Root Cause

The retrieval stage returned reviews discussing helpfulness and supportiveness, but none explicitly discussed beginner students or introductory-level teaching. Because the generation prompt enforced grounding, the model correctly refused to make unsupported assumptions.

### Potential Fix

I would collect more reviews discussing beginner experiences, increase the number of retrieved chunks, and experiment with hybrid retrieval combining semantic and keyword search.

---

## Spec Reflection

### One Way the Spec Helped

The planning document helped define the architecture before implementation. Having the retrieval strategy, chunking plan, and evaluation questions prepared in advance made development more structured and easier to debug.

### One Way the Implementation Diverged

The original plan used fixed-size character chunking with overlap. During testing, I discovered that this produced fragmented chunks that split reviews across boundaries. I switched to paragraph-based chunking because it better preserved complete student opinions and improved retrieval quality.

---

## AI Usage

### Instance 1

* **What I gave the AI:** The document structure, chunking strategy, and Milestone 3 requirements.
* **What it produced:** Python code for document loading and fixed-size chunking.
* **What I changed or overrode:** I replaced character-based chunking with paragraph-based chunking after observing fragmented chunks during testing.

### Instance 2

* **What I gave the AI:** The retrieval approach, embedding model choice, and Milestone 4 requirements.
* **What it produced:** Code for embedding chunks using all-MiniLM-L6-v2 and storing them in ChromaDB.
* **What I changed or overrode:** I added metadata-based source attribution and improved the generation prompt to better compare professors and avoid unsupported answers.
