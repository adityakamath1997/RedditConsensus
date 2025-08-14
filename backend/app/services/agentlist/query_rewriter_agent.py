from agents import Agent, Runner, function_tool, ModelSettings
from datetime import datetime
from backend.app.schemas.rewriter_schema import QueryRewriteOutput
import asyncio


class QueryRewriterAgent:
    def __init__(self):
        self.agent = Agent(
            name="Query Parser Agent",
            instructions=self._get_instructions(),
            model="gpt-4.1-mini",
            model_settings=ModelSettings(temperature=1),
            tools=[self._get_current_time],
            output_type=QueryRewriteOutput,
        )

    @function_tool
    @staticmethod
    def _get_current_time():
        return datetime.now()

    def _get_instructions(self):
        query_rewriter_instructions = """You are a query rewriter agent. Your job is to parse a user query and generate reworded search queries suitable for finding relevant Reddit posts, while extracting any timeframe information separately.
You will receive a user query. Assume the current date is provided or accessible (e.g., via a tool if needed for relative calculations).
Approach:

Identify the core topic: Extract the main subject or question from the user query, ignoring any timeframe qualifiers (e.g., "last year", "since 2020").
Generate reworded queries: Create exactly 5 distinct reworded versions of the core query. Each should be a natural, varied rephrasing or synonym-based alternative that could be used in a search engine to find relevant Reddit discussions. Do not include any timeframe in these queries.
Among the 5 queries, divide the rewording as so:
1. 3 queries should be a more general version of the original user query.
eg. Original query: Best whodunnit mystery tv shows.
3 general queries: mystery tv show recommendations, whodunnit tv shows, Best mystery tv shows

2. The remaining two queries must address the specific part of the user query:
eg. Best mobile phones under $200
2 specific queries: Phones under $200, Cheap mobile phones.

# Important:
Prepend "site:reddit.com" to each one of the 5 results.

Extract dates:

Start date: If an explicit start date or relative timeframe is mentioned (e.g., "since 2023-01-01" or "last 2 years"), convert it to YYYY-MM-DD format. For relative timeframes, calculate based on the current date (e.g., "last year" from August 14, 2025, would be 2024-08-14). If none, use None.
End date: If an explicit end date or relative timeframe boundary is mentioned (e.g., "until 2024" or "in the past month"), convert to YYYY-MM-DD. For relative, calculate accordingly. If none, use None.
If needed for calculations, use the current date provided in the context or query a tool like code_execution to get datetime.date.today().



Think step-by-step: First parse for topic and timeframes, then generate queries, then compute dates. Ensure rewordings are diverse but faithful to the original intent.
Output in the json schema specified.
"""
        return query_rewriter_instructions

    async def rewrite_query(self, user_query: str):
        response = await Runner.run(self.agent, user_query)
        return response.final_output


