from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from openai import OpenAI
from data.upsert_qdrant import save_points_to_qdrant
from dotenv import load_dotenv
import asyncio
import uuid

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


async def vectorize_text_chunks_async(contract_files: list[dict]):
    async def embed_and_log(idx, chunk, source, chunk_total):
        embedding = await get_openai_embedding(chunk)
        if embedding:
            print(f"awaited embedding for chunk... {idx + 1}/{chunk_total} >> {source}\n")
            return (embedding, {"text": chunk, "chunk_index": idx, "source": source, "chunk_id": uuid.uuid4().hex})
        return None
    
    async def embed_contract_file(file: dict):
        text = file["text"]
        source = file["source"]
        chunks = chunk_text(text)
        
        tasks = [embed_and_log(idx, chunk, source, len(chunks)) for idx, chunk in enumerate(chunks)]
        results = await asyncio.gather(*tasks)

        vectorized_chunks = [r for r in results if r is not None]
        return vectorized_chunks

    file_tasks = [embed_contract_file(file) for file in contract_files]
    file_results = await asyncio.gather(*file_tasks)

    all_vectorized_chunks = [chunk for file_result in file_results for chunk in file_result]

    print(all_vectorized_chunks)
    return all_vectorized_chunks
    

async def vectorize_to_qdrant(contract_files: list[dict]):
    vectorized_chunks = await vectorize_text_chunks_async(contract_files)
    save_points_to_qdrant(vectorized_chunks=vectorized_chunks)