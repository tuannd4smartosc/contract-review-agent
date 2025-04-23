from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from openai import OpenAI
from data.upsert_qdrant import save_points_to_qdrant
from dotenv import load_dotenv
import asyncio

load_dotenv() 

client = OpenAI()

def chunk_text(text, chunk_size=1000, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", "(?<=\\. )", " ", ""],
    )
    chunks = text_splitter.split_text(text)
    return chunks

async def get_openai_embedding(text, model="text-embedding-ada-002"):
    """Wraps the sync OpenAI call in a thread to make it async-compatible."""
    def sync_embed():
        return client.embeddings.create(input=text, model=model)

    try:
        response = await asyncio.to_thread(sync_embed)
        return response.data[0].embedding
    except Exception as e:
        print(f"Error getting OpenAI embedding: {e}")
        return None


async def vectorize_text_chunks_async(text):
    chunks = chunk_text(text)

    async def embed_and_log(idx, chunk):
        embedding = await get_openai_embedding(chunk)
        if embedding:
            print(f"awaited embedding for chunk... {idx + 1}/{len(chunks)}")
            return (embedding, {"text": chunk})
        return None

    tasks = [embed_and_log(idx, chunk) for idx, chunk in enumerate(chunks)]
    results = await asyncio.gather(*tasks)

    vectorized_chunks = [r for r in results if r is not None]
    return vectorized_chunks

async def vectorize_to_qdrant(text):
    vectorized_chunks = await vectorize_text_chunks_async(text)
    save_points_to_qdrant(vectorized_chunks=vectorized_chunks)