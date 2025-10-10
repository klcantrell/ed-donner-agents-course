from agents import Agent, agent
from research_tools import (
    ask_clarifying_questions, 
    plan_searches, 
    perform_search, 
    write_report, 
    send_email_report
)

INSTRUCTIONS = """You are a research orchestrator agent. Your job is to coordinate a deep research process.

When given a research query, you have TWO OPTIONS:

OPTION 1 - If the query is unclear, vague, or ambiguous:
- Call ask_clarifying_questions to generate 3 clarifying questions
- This will immediately stop the research process and return the questions to the user

OPTION 2 - If the query is clear and specific:
- Proceed with the normal research workflow:
  1. Call plan_searches with the query to get a list of web searches to perform
  2. For each search in the plan, call perform_search with the search query and reason
  3. Once all searches are complete, call write_report with the original query and all search results
  4. Finally, call send_email_report with the markdown report to email it

You decide which path to take based on the clarity of the query. Be systematic and thorough.
Keep track of the search results as you go and pass them all to the write_report tool.
"""

orchestrator_agent = Agent(
    name="ResearchOrchestrator",
    instructions=INSTRUCTIONS,
    tools=[ask_clarifying_questions, plan_searches, perform_search, write_report, send_email_report],
    tool_use_behavior=agent.StopAtTools(stop_at_tool_names=["ask_clarifying_questions"]),
    model="gpt-4o",
)
