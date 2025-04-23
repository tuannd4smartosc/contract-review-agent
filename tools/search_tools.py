from langchain.tools import Tool
from services.serper import google_search

google_tool = Tool(
    name="Google Search via Serper",
    func=google_search,
    description="Useful for searching for contract playbooks and related documents online."
)
