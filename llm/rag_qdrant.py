"""TEMPLATE: minimal RAG with Qdrant (in-memory, no server needed).

Shape:
  ingest: chunk -> embed -> upsert (vector + payload)
  query : embed question (SAME model) -> search top-k -> grounded prompt -> answer with sources
"""
from dotenv import load_dotenv
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

load_dotenv()
oa = OpenAI()
EMBED_MODEL, DIM = "text-embedding-3-small", 1536   # dimension must match the model
COLLECTION = "docs"
qdrant = QdrantClient(":memory:")                  # real server: QdrantClient(url="http://localhost:6333")


def chunk(text: str, size: int = 500, overlap: int = 100) -> list[str]:
    """Fixed-size chunks with overlap so sentences on a boundary aren't lost."""
    step = size - overlap
    return [text[i : i + size] for i in range(0, max(len(text) - overlap, 1), step)]


def embed(texts: list[str]) -> list[list[float]]:
    resp = oa.embeddings.create(model=EMBED_MODEL, input=texts)   # batch call, one request
    return [d.embedding for d in resp.data]


def ingest(docs: dict[str, str]) -> None:
    if qdrant.collection_exists(COLLECTION):
        qdrant.delete_collection(COLLECTION)            # fresh index each run (demo)
    qdrant.create_collection(COLLECTION, vectors_config=VectorParams(size=DIM, distance=Distance.COSINE))
    points, pid = [], 0
    for source, text in docs.items():
        chunks = chunk(text)
        for c, vec in zip(chunks, embed(chunks)):
            points.append(PointStruct(id=pid, vector=vec, payload={"text": c, "source": source}))
            pid += 1
    qdrant.upsert(COLLECTION, points)


def answer(question: str, k: int = 3) -> str:
    hits = qdrant.query_points(COLLECTION, query=embed([question])[0], limit=k).points
    context = "\n\n".join(f"[{h.payload['source']}] {h.payload['text']}" for h in hits)
    resp = oa.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": "Answer ONLY from the context. Cite [source]. "
                                          "If the answer is not there, say you don't know."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
    )
    return resp.choices[0].message.content


if __name__ == "__main__":
    ingest({"policy.txt": "Refunds are allowed within 30 days of purchase with a receipt. "
                          "Digital goods are non-refundable once downloaded."})
    print(answer("Can I get a refund on an ebook I downloaded?"))
