from pathlib import Path

DOCUMENT_FOLDER = "documents"

CHUNK_SIZE = 300
OVERLAP = 50


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


documents = load_documents()

all_chunks = []

for doc in documents:

    chunks = chunk_text(doc["text"])

    for i, chunk in enumerate(chunks):

        all_chunks.append({
            "source": doc["source"],
            "chunk_id": i,
            "text": chunk
        })

print(f"\nTotal chunks: {len(all_chunks)}\n")

for chunk in all_chunks[:5]:
    print(chunk["source"])
    print(chunk["text"])
    print("=" * 60)