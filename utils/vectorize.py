from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from openai import OpenAI
from data.qdrant import save_points_to_qdrant
from dotenv import load_dotenv

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

def get_openai_embedding(text, model="text-embedding-ada-002"):
    """Gets the OpenAI embedding for a given text."""
    try:
        response = client.embeddings.create(
            input=text,
            model=model
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error getting OpenAI embedding: {e}")
        return None


def vectorize_text_chunks(text):
    chunks = chunk_text(text)
    vectorized_chunks = []
    for idx, chunk in enumerate(chunks):
        embedding = get_openai_embedding(chunk)
        print("embedded chunk...", chunk, idx)
        if embedding:
            vectorized_chunks.append(embedding)
    return vectorized_chunks

def vectorize_to_qdrant(text):
    vectorized_chunks = vectorize_text_chunks(text)
    save_points_to_qdrant(vectorized_chunks=vectorized_chunks)