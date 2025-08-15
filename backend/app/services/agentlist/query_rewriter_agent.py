from agents import Agent, Runner, function_tool, ModelSettings, AgentOutputSchema
from datetime import datetime
from app.schemas.rewriter_schema import QueryRewriteOutput
import asyncio
from agents.extensions.models.litellm_model import LitellmModel

class QueryRewriterAgent:
    def __init__(self):
        self.agent = Agent(
            name="Query Parser Agent",
            instructions=self._get_instructions(),
            model="o4-mini",
            tools=[self._get_current_time],
            output_type=AgentOutputSchema(QueryRewriteOutput),
        )

    @function_tool
    @staticmethod
    def _get_current_time():
        return datetime.now()

    def _get_instructions(self):
        query_rewriter_instructions = """You are a query rewriter agent. Your job is to parse a user query and generate reworded search queries suitable for finding relevant Reddit posts, while extracting any timeframe information separately.
You will receive a user query. Assume the current date is provided or accessible (e.g., via a tool if needed for relative calculations).
Approach:

# Important:
Extract the main query: The timeframe DOES NOT go into the main query.
The main query extracted will be the first query.
After this, generate reworded queries: Create exactly 5 distinct reworded versions of the core query. Each should be a natural, varied rephrasing or synonym-based alternative that could be used in a search engine to find relevant Reddit discussions. Do not include any timeframe in these queries.
Be general as opposed to specific, try to reword the original query in such a manner that the reworded queries will find more Reddit discussions about topics relevant to what the user is asking.

One-shot example:

eg. Best sitcoms of the last 20 years.

Reworded queries: best sitcoms, funny tv shows, sitcom recommendations, comedy tv shows, best sitcom you've seen.

Note how the timeframe is NOT inthe query.
Extract dates:

Start date: If an explicit start date or relative timeframe is mentioned (e.g., "since 2023-01-01" or "last 2 years"), convert it to YYYY-MM-DD format. For relative timeframes, calculate based on the current date (e.g., "last year" from August 14, 2025, would be 2024-08-14). If none, use None.
End date: If an explicit end date or relative timeframe boundary is mentioned (e.g., "until 2024" or "in the past month"), convert to YYYY-MM-DD. For relative, calculate accordingly. If none, use None.
If needed for calculations, use the current date provided in the context or query a tool like code_execution to get datetime.date.today().



Think step-by-step: First parse for topic and timeframes, then generate queries, then compute dates. Ensure rewordings are diverse but faithful to the original intent.
Output in the json schema specified. You will return 6 queries, the original extracted query, and 5 reworded queries.
"""
        return query_rewriter_instructions

    async def rewrite_query(self, user_query: str):
        response = await Runner.run(self.agent, user_query)
        return response.final_output


