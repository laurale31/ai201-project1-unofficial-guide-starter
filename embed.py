from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb

DOCUMENT_FOLDER = "documents"

# ---------- Load Documents ----------

def load_documents():
    docs = []

    for file_path in Path(DOCUMENT_FOLDER).glob("*.txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        docs.append({
            "source": file_path.name,
            "text": text
        })

    return docs

# ---------- Chunk Documents ----------

def chunk_text(text):
    paragraphs = text.split("\n\n")

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:

        if len(current_chunk) + len(paragraph) < 300:
            current_chunk += paragraph + "\n\n"

        else:
            chunks.append(current_chunk.strip())
            current_chunk = paragraph + "\n\n"

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

# ---------- Load Embedding Model ----------

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------- ChromaDB ----------

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="professor_reviews"
)

# ---------- Process Documents ----------

documents = load_documents()

chunk_count = 0

for doc in documents:

    chunks = chunk_text(doc["text"])

    for i, chunk in enumerate(chunks):

        embedding = model.encode(chunk).tolist()

        collection.add(
            ids=[f"{doc['source']}_{i}"],
            embeddings=[embedding],
            documents=[chunk],
            metadatas=[{
                "source": doc["source"]
            }]
        )

        chunk_count += 1

print(f"\nStored {chunk_count} chunks in ChromaDB")