from sentence_transformers import SentenceTransformer
import chromadb

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load ChromaDB
client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection(
    name="professor_reviews"
)

query = input("Question: ")

query_embedding = model.encode(query).tolist()

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5
)

print("\nTOP RESULTS\n")

for i in range(len(results["documents"][0])):

    print(f"Result {i+1}")

    print(
        "Source:",
        results["metadatas"][0][i]["source"]
    )

    print(
        results["documents"][0][i]
    )

    print("-" * 60)