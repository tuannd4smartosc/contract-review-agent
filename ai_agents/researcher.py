from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
from tools.search_tools import google_tool

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

system_message = """
    You are a legal research assistant specializing in contracts. Your task is to find publicly available contract playbooks for different legal agreements such as NDAs, MSAs, and SOWs.
    Your responses should be concise and focused on the most relevant and trustworthy PDF files.
"""

researcher_agent = initialize_agent(
    tools=[google_tool],
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True,
    system_message=system_message
)
