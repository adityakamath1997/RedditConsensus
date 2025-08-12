# tests/test_tavily_client.py
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import pytest
from unittest.mock import Mock, patch
from backend.app.services.tavily_client import TavilySearch


class TestTavilySearch:
    @pytest.mark.asyncio
    @patch("backend.app.services.tavily_client.TavilyClient")
    async def test_successful_search(self, mock_client):
        # Mock the response
        mock_client.return_value.search.return_value = {"results": [...]}

        client = TavilySearch()
        results = await client.tavily_search(
            ["test query"], 5, "2024-01-01", "2024-01-31"
        )

        assert len(results) == 1
        assert results[0] is not None

    @pytest.mark.asyncio
    @patch("backend.app.services.tavily_client.TavilyClient")
    async def test_partial_failure(self, mock_client):
        # First call succeeds, second fails
        mock_client.return_value.search.side_effect = [
            {"results": [...]},
            Exception("API Error"),
        ]

        client = TavilySearch()
        results = await client.tavily_search(["good", "bad"], 5, None, None)

        assert len(results) == 2
        assert results[0] is not None
        assert results[1] is None
