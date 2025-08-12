from fastapi import APIRouter, HTTPException
from backend.app.services.search_service import SearchService
from backend.app.schemas.api import SearchRequest, SearchResponse
import asyncio

router = APIRouter(prefix="/api/v1", tags=["search"])


@router.post("/search", response_model=SearchResponse)
async def search_reddit_consensus(request: SearchRequest):
    try:
        search_service = SearchService()
        result = await search_service.search(
            user_query=request.query, max_results=request.max_results
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
