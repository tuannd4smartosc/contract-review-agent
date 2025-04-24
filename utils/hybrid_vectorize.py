from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import uuid

client = QdrantClient("http://localhost:6333")
collection_name = "hybrid_search_collection"

async def vectorize_hybrid(documents: list[dict]):
    # Dense vectors
    dense_model = SentenceTransformer("all-MiniLM-L6-v2")
    dense_vectors = dense_model.encode([doc["text"] for doc in documents])

    # Sparse vectors
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform([doc["text"] for doc in documents])
    sparse_vectors = [
        models.SparseVector(indices=m.indices.tolist(), values=m.data.tolist())
        for m in tfidf_matrix
    ]

    # Upload to Qdrant
    points = [
        models.PointStruct(
            id=doc["id"],
            vector={"dense": dense_vectors[i].tolist(), "sparse": sparse_vectors[i]},
            payload={"text": doc["text"], "chunk_index": i, "source": doc["source"], "chunk_id": uuid.uuid4().hex}
        )
        for i, doc in enumerate(documents)
    ]
    client.upsert(collection_name=collection_name, points=points)