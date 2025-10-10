from typing import List
from pydantic import BaseModel, Field
from agents import Agent, Runner, function_tool


class ClarifyingQuestions(BaseModel):
    """Model for clarifying questions about a research query"""
    questions: List[str] = Field(description="List of exactly 3 clarifying questions")


# Agent for generating clarifying questions
clarifying_agent = Agent(
    name="ClarifyingQuestionsAgent",
    instructions=(
        "You are a research assistant that helps clarify vague or ambiguous research queries. "
        "Analyze the given query and generate exactly 3 specific, targeted clarifying questions "
        "that would help make the research more focused and effective. "
        "Questions should address scope, specific aspects, time frames, geographic regions, or other relevant details."
    ),
    model="gpt-4o-mini",
    output_type=ClarifyingQuestions,
)


@function_tool
async def ask_clarifying_questions(query: str) -> ClarifyingQuestions:
    """
    Generate 3 clarifying questions about the research query.
    Use this tool when the query is vague, ambiguous, or lacks sufficient detail.
    
    Args:
        query: The research query to ask clarifying questions about
        
    Returns:
        ClarifyingQuestions containing exactly 3 clarifying questions
    """
    print("Generating clarifying questions...")
    result = await Runner.run(
        clarifying_agent,
        f"Research query: {query}",
    )
    clarifying_questions = result.final_output_as(ClarifyingQuestions)
    print(f"Generated {len(clarifying_questions.questions)} clarifying questions")
    
    return clarifying_questions
