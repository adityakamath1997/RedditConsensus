import asyncio
from backend.app.services.agentlist.query_rewriter_agent import QueryRewriterAgent
from backend.app.services.agentlist.consensus_agent import ConsensusAgent
from backend.app.services.agentlist.metrics_agent import MetricsAgent
from backend.app.services.reddit_client import RedditClient
from backend.app.services.tavily_client import TavilySearch
from agents import trace
from backend.app.services.plot_service import build_histogram_images
from dotenv import load_dotenv
from pprint import pprint
from colorama import Fore
import os

load_dotenv()

class SearchService:
    def __init__(self, comment_depth=10, model="gpt-4.1-mini"):
        self.model = model
        self.query_rewriter = QueryRewriterAgent()
        self.tavily_client = TavilySearch()
        self.reddit_client = RedditClient(comment_depth)
        
        
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

        print(f"Generating consensus and metrics from {len(post_details)} posts...")
        consensus_agent = ConsensusAgent(original_query=user_query, post_details=post_details, model=self.model)
        metrics_agent = MetricsAgent(original_query=user_query, post_details=post_details, model=self.model)


        consensus, metrics = await asyncio.gather(
            consensus_agent.get_consensus(), metrics_agent.get_metrics(),
        )   

        histogram_images = build_histogram_images(metrics, max_bars=15)

        return {
            "original_query": user_query,
            "start_date": rewrite_result.start_date,
            "end_date": rewrite_result.end_date,
            "posts_analyzed": len(post_details),
            "reddit_urls": reddit_urls,  # Add the list of URLs
            "consensus": consensus,
            "metrics": metrics,
            "answer_frequency_png": histogram_images.get("answer_frequency_png"),
            "like_count_png": histogram_images.get("like_count_png"),
        }

