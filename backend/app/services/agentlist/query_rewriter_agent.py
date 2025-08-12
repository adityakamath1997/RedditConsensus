from agents import Agent, Runner, function_tool
from datetime import datetime
from backend.app.schemas.rewriter_schema import QueryRewriteOutput
import asyncio


class QueryRewriterAgent:
    def __init__(self):
        self.agent = Agent(
            name="Query Parser Agent",
            instructions=self._get_instructions(),
            model="gpt-4.1-mini",
            tools=[self._get_current_time],
            output_type=QueryRewriteOutput,
        )

    @function_tool
    @staticmethod
    def _get_current_time():
        return datetime.now()

    def _get_instructions(self):
        query_rewriter_instructions = """
Your job is to take a user query, and parse it, you will return the following:

1. A list of 3 reworded queries of the thing the user is looking for, where each query is the original query rewritten in a different manner or a similar query that will be used in a search engine to find relevant posts.
#IMPORTANT: THE TIMEFRAME DOESN'T GO INTO THE REWORDED QUERY, ONLY THE ORIGINAL QUERY.
2. #IMPORTANT: prepend "site:reddit.com" to each of the generated queries.
eg. Best bugdget gaming laptops in the past 5 years. Reworded queries: site:reddit.com Affordable gaming laptops, site:reddit.com cheap gaming laptops, site:reddit.com inexpensive laptops
2. A start date if mentioned by the user in YYYY-MM-DD format, else None
3. An end date mentioned by the user in YYYY-MM-DD format, else None

Use the _get_current_time tool to find current time
"""
        return query_rewriter_instructions

    async def rewrite_query(self, user_query: str):
        response = await Runner.run(self.agent, user_query)
        return response.final_output


if __name__ == "__main__":

    async def main():
        rewriter = QueryRewriterAgent()
        print(await rewriter.rewrite_query("test"))

    asyncio.run(main())
