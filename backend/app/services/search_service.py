import asyncio
from app.services.agentlist.query_rewriter_agent import QueryRewriterAgent
from app.services.agentlist.consensus_agent import ConsensusAgent
from app.services.agentlist.metrics_agent import MetricsAgent
from app.services.agentlist.relevance_checker_agent import RelevanceCheckerAgent
from app.services.reddit_client import RedditClient
from app.services.tavily_client import TavilySearch
from agents import trace
from app.services.plot_service import build_histogram_images
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
        rewrite_result = await self.query_rewriter.rewrite_query(user_query)
        original_query = rewrite_result.queries[0]
        
        reddit_urls = await self.tavily_client.tavily_search(
            queries=rewrite_result.queries,
            max_results=max_results,
            start_date=rewrite_result.start_date,
            end_date=rewrite_result.end_date,
        )
        relevance_agent = RelevanceCheckerAgent(original_query=original_query)

        relevance_check = await relevance_agent.get_relevance(reddit_urls)

        relevant_reddit_urls = [url for url, flag in zip(reddit_urls, relevance_check) if flag]


        if not reddit_urls:
            return f"Error: No Reddit posts found"


        post_details = await self.reddit_client.get_posts_content(relevant_reddit_urls)

        if not post_details:
            return {"error": "Could not fetch post content"}

        consensus_agent = ConsensusAgent(original_query=original_query, post_details=post_details, model=self.model)
        metrics_agent = MetricsAgent(original_query=original_query, post_details=post_details, model=self.model)


        consensus, metrics = await asyncio.gather(
            consensus_agent.get_consensus(), metrics_agent.get_metrics(),
        )   

        histogram_images = build_histogram_images(metrics, max_bars=15)

        return {
            "original_query": user_query,
            "start_date": rewrite_result.start_date,
            "end_date": rewrite_result.end_date,
            "posts_analyzed": len(post_details),
            "reddit_urls": relevant_reddit_urls,  # Relevant URLs only
            "consensus": consensus,
            "metrics": metrics,
            "answer_frequency_png": histogram_images.get("answer_frequency_png"),
            "like_count_png": histogram_images.get("like_count_png"),
        }

