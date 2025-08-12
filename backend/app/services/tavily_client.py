import asyncio
import os
import re
from tavily import TavilyClient

class TavilySearch:
    def __init__(self):
        self.client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        self.reddit_pattern = re.compile(
            r"^(?:https?://)?(?:www\.|old\.)?reddit\.com/r/[^/]+/comments/[a-z0-9]+(?:/[^/]+)?/?$"
            r"|^(?:https?://)?redd\.it/[a-z0-9]+/?$",
            re.IGNORECASE
        )
        self.seen_urls = set()

    async def tavily_search(self, queries: list[str], max_results, start_date, end_date):
        loop = asyncio.get_event_loop()
        
        tasks = [
            loop.run_in_executor(None, self._single_search, query, max_results, start_date, end_date)
            for query in queries
        ]
        
        results = await asyncio.gather(*tasks)

        unique_results = []
        for result in results:
            if result and 'results' in result:
                for item in result['results']:
                    url = item.get('url', '')
                    if url not in self.seen_urls:
                        self.seen_urls.add(url)
                        unique_results.append(url)
        
        return unique_results

    def _single_search(self, query, max_results, start_date, end_date):
        try:
            result = self.client.search(
                query=query,
                max_results=max_results,
                start_date=start_date,
                end_date=end_date,
            )
            
            
            if result and 'results' in result:
                reddit_results = [
                    item for item in result['results'] 
                    if self._is_reddit_url(item.get('url', ''))
                ]
                result['results'] = reddit_results
            
            return result
        except Exception as e:
            print(f"Search failed for '{query}': {e}")
            return None

    def _is_reddit_url(self, url):
        return bool(self.reddit_pattern.match(url))

if __name__ == "__main__":
    import asyncio
    from dotenv import load_dotenv
    from pprint import pprint
    
    async def quick_test():
        load_dotenv()
        
        client = TavilySearch()
        queries = ["site:reddit.com Best budget laptops", "javascript"]
        
        print("Testing Tavily client...")
        results = await client.tavily_search(queries, 10, "2025-02-02", "2025-08-03")
        
        print(f"Got {len(results)} unique results:")
        for i, item in enumerate(results):
            print(f"  Result {i+1}: {item.get('url', 'No URL')}")
            
    asyncio.run(quick_test())
