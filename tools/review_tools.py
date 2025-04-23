from langchain.tools import tool
from langchain.chat_models import ChatOpenAI
from data.retrieve_qdrant import retrieve_relevant_chunks
from langchain.schema import HumanMessage
import asyncio

llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

@tool
def extract_clauses(text: str) -> str:
    """Extracts standard legal clauses from a contract."""
    relevant_chunks = asyncio.run(retrieve_relevant_chunks("standard contract clauses"))
    context = "\n---\n".join(relevant_chunks)
    prompt = f"""
        Use the following examples of clauses from contract playbooks and past contracts to extract similar clauses from this input.

        [Context knowledge base]
        {context}

        [Contract to analyze]
        {text}

        Return a list of identified clause names with short summaries.
    """
    return llm([HumanMessage(content=prompt)]).content

@tool
def check_missing_clauses(text: str) -> str:
    """Checks missing clauses using knowledge base as checklist reference."""
    relevant_chunks = asyncio.run(retrieve_relevant_chunks("full list of standard clauses in NDA, MSA, SOW"))
    context = "\n---\n".join(relevant_chunks)
    prompt = f"""
        Use the following reference clause checklist and examples to analyze the contract.

        [Reference clauses from KB]
        {context}

        [Contract to analyze]
        {text}

        List the clauses that appear to be missing.
    """
    return llm([HumanMessage(content=prompt)]).content

@tool
def summarize_contract(text: str) -> str:
    """Summarizes a contract in simple terms using prior examples."""
    relevant_chunks = asyncio.run(retrieve_relevant_chunks("how to summarize contracts for business users"))
    context = "\n---\n".join(relevant_chunks)

    prompt = f"""
    Use the examples below to summarize this contract in plain English.

    [Examples]
    {context}

    [Contract]
    {text}
    """
    return llm([HumanMessage(content=prompt)]).content


@tool
def create_tasks(text: str) -> str:
    """Create a list of tasks to improve the contract based on real-life contract requirements."""

    prompt = f"""
    Create a plan of to-do items to improve the contract.

    [Contract]
    {text}
    """
    return llm([HumanMessage(content=prompt)]).content