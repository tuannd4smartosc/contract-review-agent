from data.qdrant import qdrant_client, collection_name
from qdrant_client import models

def save_points_to_qdrant(vectorized_chunks, batch_size=100):
    if not vectorized_chunks:
        print("No chunks vectorized with OpenAI to store.")
        return

    vector_dimension = len(vectorized_chunks[0][0])

    qdrant_client.recreate_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=vector_dimension, distance=models.Distance.COSINE),
    )

    for i in range(0, len(vectorized_chunks), batch_size):
        batch = vectorized_chunks[i:i + batch_size]
        points = [
            models.PointStruct(id=i + j, vector=vector, payload=metadata)
            for j, (vector, metadata) in enumerate(batch)
        ]

        qdrant_client.upsert(
            collection_name=collection_name,
            points=points,
            wait=True,
        )
        print(f"Batch {i//batch_size + 1}: Upserted {len(points)} vectors")
        
