import pytest


@pytest.mark.asyncio
async def test_search_service_happy_path(monkeypatch):
    from backend.app.services.search_service import SearchService
    from backend.app.services.agentlist.query_rewriter_agent import QueryRewriterAgent
    from backend.app.services.agentlist.consensus_agent import ConsensusAgent
    from backend.app.services.agentlist.metrics_agent import MetricsAgent
    from backend.app.services.tavily_client import TavilySearch
    from backend.app.services.reddit_client import RedditClient
    import backend.app.services.search_service as search_service_module

    class DummyRewriteResult:
        def __init__(self):
            self.queries = ["q1", "q2"]
            self.start_date = "2020-01-01"
            self.end_date = "2024-01-01"

    async def mock_rewrite_query(self, user_query: str):
        return DummyRewriteResult()

    async def mock_tavily_search(self, queries, max_results, start_date, end_date):
        assert isinstance(queries, list)
        assert max_results == 2
        return [
            "https://www.reddit.com/r/test/comments/abc1",
            "https://www.reddit.com/r/test/comments/abc2",
        ]

    async def mock_get_posts_content(self, reddit_url_list):
        return [
            "POST 1:\nTitle: T1\nAuthor: A1\nContent: C1\n\nTop Comments:\n1. (5 upvotes) Comment one\n",
            "POST 2:\nTitle: T2\nAuthor: A2\nContent: C2\n\nTop Comments:\n1. (3 upvotes) Comment two\n",
        ]

    def mock_get_comments_and_upvotes(self):
        return [("Comment one", 5), ("Comment two", 3)]

    async def mock_get_consensus(self):
        return {
            "consensus": "Test consensus",
            "additional_info": {
                "reasons": ["r1", "r2"],
                "caveats": ["c1"],
            },
        }

    async def mock_get_metrics(self):
        return {
            "answer_frequency": {"A": 2, "B": 1},
            "like_count": {"A": 10, "B": 4},
        }

    def mock_build_histogram_images(metrics, max_bars: int = 15):
        assert "answer_frequency" in metrics and "like_count" in metrics
        return {
            "answer_frequency_png": "dGVzdA==",
            "like_count_png": "dGVzdA==",
        }

    # Apply monkeypatches
    monkeypatch.setattr(QueryRewriterAgent, "rewrite_query", mock_rewrite_query, raising=True)
    monkeypatch.setattr(TavilySearch, "tavily_search", mock_tavily_search, raising=True)
    monkeypatch.setattr(RedditClient, "get_posts_content", mock_get_posts_content, raising=True)
    monkeypatch.setattr(RedditClient, "get_comments_and_upvotes", mock_get_comments_and_upvotes, raising=True)
    monkeypatch.setattr(ConsensusAgent, "get_consensus", mock_get_consensus, raising=True)
    monkeypatch.setattr(MetricsAgent, "get_metrics", mock_get_metrics, raising=True)
    monkeypatch.setattr(search_service_module, "build_histogram_images", mock_build_histogram_images, raising=True)

    service = SearchService()
    result = await service.search(user_query="test query", max_results=2)

    assert result["original_query"] == "test query"
    assert result["posts_analyzed"] == 2
    assert len(result.get("reddit_urls", [])) == 2

    assert "consensus" in result
    assert result["consensus"]["consensus"] == "Test consensus"
    assert "additional_info" in result["consensus"]

    assert "metrics" in result
    assert "answer_frequency" in result["metrics"]
    assert "like_count" in result["metrics"]

    assert result.get("answer_frequency_png")
    assert result.get("like_count_png")


