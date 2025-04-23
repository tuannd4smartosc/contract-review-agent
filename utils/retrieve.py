from openai import AsyncOpenAI
from data.retrieve_qdrant import retrieve_relevant_chunks

client = AsyncOpenAI()

async def generate_answer(query):
    relevant_chunks = await retrieve_relevant_chunks(query)
    context = "\n---\n".join(relevant_chunks)
    print("context",context)
    prompt = f"""You are an expert assistant. Use the following context to answer the question.
    
    Context:
    {context}

    Question: {query}
    Answer:"""

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()
