from data.qdrant import qdrant_client, collection_name
from qdrant_client.models import SearchParams
from utils.vectorize import get_openai_embedding

async def retrieve_relevant_chunks(query, top_k=5):
    query_vector = await get_openai_embedding(query)

    search_results = qdrant_client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=top_k,
        search_params=SearchParams(hnsw_ef=128),
    )

    return [hit.payload["text"] for hit in search_results]