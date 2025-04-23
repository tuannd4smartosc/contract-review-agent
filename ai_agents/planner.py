from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
from tools.review_tools import extract_clauses, check_missing_clauses, summarize_contract, create_tasks

llm = ChatOpenAI(model="gpt-3.5-turbo",temperature=0)

planner_agent = initialize_agent(
    tools= [ extract_clauses, check_missing_clauses, summarize_contract, create_tasks],
    llm = llm,
    agent="zero-shot-react-description",
    verbose=True
)