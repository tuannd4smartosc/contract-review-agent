from qdrant_client import QdrantClient

qdrant_client = QdrantClient("http://localhost:6333") 
collection_name = "doc_vectors"