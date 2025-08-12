import asyncio
from backend.app.services.agentlist.query_rewriter_agent import QueryRewriterAgent
from backend.app.services.agentlist.consensus_agent import ConsensusAgent
from backend.app.services.reddit_client import RedditClient
from backend.app.services.tavily_client import TavilySearch
from dotenv import load_dotenv
from pprint import pprint
from colorama import Fore

class SearchService:
    def __init__(self):
        self.query_rewriter = QueryRewriterAgent()
        self.tavily_client = TavilySearch()
        self.reddit_client = RedditClient()

    async def search(self, user_query: str, max_results: int = 5):
        print(f"Rewriting query: {user_query}")
        rewrite_result = await self.query_rewriter.rewrite_query(user_query)

        print(f"Queries: {rewrite_result.queries}")
        print(f"Start date: {rewrite_result.start_date} to {rewrite_result.end_date}")

        print(f"Searching with Tavily...")
        reddit_urls = await self.tavily_client.tavily_search(
            queries=rewrite_result.queries,
            max_results=max_results,
            start_date=rewrite_result.start_date,
            end_date=rewrite_result.end_date,
        )

        if not reddit_urls:
            return f"Error: No Reddit posts found"
        
        print(f"Found {len(reddit_urls)} Reddit URLs. Fetching post content...")
        post_details = await self.reddit_client.get_posts_content(reddit_urls)

        print(Fore.MAGENTA + f"{post_details}" + Fore.RESET)

        if not post_details:
            return {"error": "Could not fetch post content"}

        print(f"Generating consensus from {len(post_details)} posts...")
        consensus_agent = ConsensusAgent(original_query=user_query)  
        consensus = await consensus_agent.get_consensus(post_details)

        return {
            "original_query": user_query,
            "start_date": rewrite_result.start_date,
            "end_date": rewrite_result.end_date,
            "posts_analyzed": len(post_details),
            "reddit_urls": reddit_urls,  # Add the list of URLs
            "consensus": consensus
        }
        


if __name__ == "__main__":

    async def main():
        orchestrator = SearchService()
        result = await orchestrator.search(
            user_query="Friendliest dog breeds",
            max_results=10
        )

        print(Fore.GREEN + f"{result}" + Fore.RESET)

    asyncio.run(main())
