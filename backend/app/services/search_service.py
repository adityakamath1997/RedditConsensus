import asyncio
from backend.app.services.agentlist.query_rewriter import QueryRewriterAgent
from backend.app.services.tavily_client import TavilySearch
from dotenv import load_dotenv

load_dotenv()

class SearchService:
    def __init__(self):
        self.query_rewriter = QueryRewriterAgent()
        self.tavily_client = TavilySearch()

    async def search(self, user_query: str, max_results: int = 5):
        print(f"Rewriting query: {user_query}")
        rewrite_result = await self.query_rewriter.rewrite_query(user_query)

        print(f"Queries: {rewrite_result.queries}")
        print(f"Start date: {rewrite_result.start_date} to {rewrite_result.end_date}")

        print(f"Searching with Tavily...")
        search_results = await self.tavily_client.tavily_search(
            queries=rewrite_result.queries,
            max_results=max_results,
            start_date=rewrite_result.start_date,
            end_date=rewrite_result.end_date,
        )

        return search_results


if __name__ == "__main__":

    async def main():
        orchestrator = SearchService()
        result = await orchestrator.search(
            user_query="Best budget gaming laptops in the last 3 months",
            max_results=10
        )
        print(f"Found {len(result)} reddit posts: /n/n")
        for res in result:
            print(res)
        print(type(result))
    asyncio.run(main())
