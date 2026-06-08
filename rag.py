import os

from dotenv import load_dotenv
from groq import Groq

from sentence_transformers import SentenceTransformer
import chromadb

load_dotenv()

# -----------------------
# GROQ
# -----------------------

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# -----------------------
# EMBEDDING MODEL
# -----------------------

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# -----------------------
# CHROMADB
# -----------------------

db = chromadb.PersistentClient(
    path="chroma_db"
)

collection = db.get_collection(
    name="professor_reviews"
)

# -----------------------
# ASK FUNCTION
# -----------------------

def ask(question):

    query_embedding = embedding_model.encode(
        question
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )

    chunks = results["documents"][0]

    sources = []

    for meta in results["metadatas"][0]:
        sources.append(meta["source"])

    context = "\n\n".join(chunks)

    prompt = f"""
You are answering questions about professor reviews.

Use ONLY the provided context.

When multiple professors are mentioned:
- Compare them.
- Explain which professor best matches the question.
- Quote specific evidence from the reviews.

If the context does not contain enough information, respond:

"I don't have enough information to answer."

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response.choices[0].message.content

    return answer, sources

# -----------------------
# TEST
# -----------------------

if __name__ == "__main__":

    question = input("Question: ")

    answer, sources = ask(question)

    print("\nANSWER\n")
    print(answer)

    print("\nSOURCES\n")

    for s in sorted(set(sources)):
        print(f"• {s}")