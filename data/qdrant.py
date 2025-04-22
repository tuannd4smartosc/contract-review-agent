from qdrant_client import QdrantClient, models
from qdrant_client.models import VectorParams, Distance

qdrant_client = QdrantClient("http://localhost:6333") 
collection_name = "doc_vectors"

def save_points_to_qdrant(vectorized_chunks):
    vector_dimension_openai = len(vectorized_chunks[0][0]) if vectorized_chunks else None

    if vector_dimension_openai:
        qdrant_client.recreate_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=vector_dimension_openai, distance=models.Distance.COSINE),
        )

        points = []
        for i, (vector, metadata) in enumerate(vectorized_chunks):
            points.append(models.PointStruct(id=i, vector=vector, payload=metadata))

        operation_info = qdrant_client.upsert(collection_name=collection_name, points=points, wait=True)
        print(f"Upsert operation status (OpenAI): {operation_info.status}")
        print(f"Successfully upserted {len(points)} vectors to Qdrant collection '{collection_name}'.")
    else:
        print("No chunks vectorized with OpenAI to store.")