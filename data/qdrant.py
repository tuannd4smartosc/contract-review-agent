from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

# Initialize Qdrant client
qdrant_client = QdrantClient("http://localhost:6333")  # Replace with your Qdrant URL

# Create collection (if not exists)
collection_name = "doc_vectors"
qdrant_client.recreate_collection(
    collection_name=collection_name,
    vector_params=VectorParams(size=1536, distance=Distance.COSINE),  # Adjust the size based on your embedding model
)
