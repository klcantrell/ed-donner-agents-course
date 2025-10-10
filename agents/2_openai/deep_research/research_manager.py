from agents import Runner, trace, gen_trace_id
from orchestrator_agent import orchestrator_agent
from clarifying_agent import ClarifyingQuestions
from writer_agent import ReportData

class ResearchManager:

    async def run(self, query: str):
        """ Run the deep research process, yielding the status updates and the final report"""
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
            yield "Starting research with orchestrator agent..."
            
            # Run the orchestrator agent which will use tools to complete the research
            result = await Runner.run(
                orchestrator_agent,
                f"Research query: {query}",
            )
            
            # Check if the agent returned clarifying questions or a report
            final_output = result.final_output
            
            if isinstance(final_output, ClarifyingQuestions):
                # Agent asked clarifying questions - format them for display
                yield "## Clarifying Questions\n\n"
                yield "Please provide more details to help with the research:\n\n"
                for i, question in enumerate(final_output.questions, 1):
                    yield f"{i}. {question}\n\n"
            elif isinstance(final_output, ReportData):
                # Agent completed the research - show the report
                yield "Research complete"
                yield final_output.markdown_report
            else:
                # Fallback for any other output format
                yield "Research complete"
                yield str(final_output)
