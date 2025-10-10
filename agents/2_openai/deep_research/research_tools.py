from typing import List
from agents import Runner, function_tool
from planner_agent import planner_agent, WebSearchPlan
from search_agent import search_agent
from writer_agent import writer_agent, ReportData
from email_agent import email_agent, EmailResult
from clarifying_agent import ask_clarifying_questions


@function_tool
async def plan_searches(query: str) -> WebSearchPlan:
    """
    Plan the web searches needed to answer a research query.
    
    Args:
        query: The research query to plan searches for
        
    Returns:
        A WebSearchPlan containing the list of searches with reasons and queries
    """
    print("Planning searches...")
    result = await Runner.run(
        planner_agent,
        f"Query: {query}",
    )
    search_plan = result.final_output_as(WebSearchPlan)
    print(f"Will perform {len(search_plan.searches)} searches")
    
    return search_plan


@function_tool
async def perform_search(search_query: str, reason: str) -> str:
    """
    Perform a web search and return a concise summary.
    
    Args:
        search_query: The search term to use
        reason: The reason for performing this search
        
    Returns:
        A concise summary of the search results
    """
    input_text = f"Search term: {search_query}\nReason for searching: {reason}"
    try:
        result = await Runner.run(
            search_agent,
            input_text,
        )
        return str(result.final_output)
    except Exception as e:
        return f"Search failed: {str(e)}"


@function_tool
async def write_report(query: str, search_results: List[str]) -> ReportData:
    """
    Write a comprehensive research report based on search results.
    
    Args:
        query: The original research query
        search_results: List of summarized search results
        
    Returns:
        ReportData containing the report summary, full markdown report, and follow-up questions
    """
    print("Writing report...")
    input_text = f"Original query: {query}\nSummarized search results: {search_results}"
    result = await Runner.run(
        writer_agent,
        input_text,
    )
    
    report_data = result.final_output_as(ReportData)
    print("Finished writing report")
    
    return report_data


@function_tool
async def send_email_report(markdown_report: str) -> EmailResult:
    """
    Send the research report via email.
    
    Args:
        markdown_report: The markdown formatted report to send
        
    Returns:
        EmailResult with the status of the email send operation
    """
    print("Sending email...")
    result = await Runner.run(
        email_agent,
        markdown_report,
    )
    print("Email sent")
    # The email_agent returns the EmailResult directly
    return result.final_output_as(EmailResult)
