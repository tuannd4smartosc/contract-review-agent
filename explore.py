from ai_agents.researcher import researcher_agent

response = researcher_agent.run(
    "Find 50 PDF contract samples for NDA, MSA, and SOW agreements. Prefer legal professional sources. The references must be PDF links."
)
print("response",response)