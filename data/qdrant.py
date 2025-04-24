from qdrant_client import QdrantClient, models
from qdrant_client.models import SearchParams
from utils.vectorize import get_openai_embedding

qdrant_client = QdrantClient("http://localhost:6333") 
collection_name = "doc_vectors"

async def retrieve_relevant_chunks(query, top_k=5):
    query_vector = await get_openai_embedding(query)

    search_results = qdrant_client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=top_k,
        search_params=SearchParams(hnsw_ef=128),
    )

    return [hit.payload["text"] for hit in search_results]



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
        
