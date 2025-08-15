from fastapi import APIRouter, HTTPException, Request
from app.services.search_service import SearchService
from app.schemas.api import SearchRequest, SearchResponse
from app.errors import RateLimitError, ServiceUnavailableError, UpstreamError, InternalServerError
from slowapi.util import get_remote_address
from app.main import limit_er

router = APIRouter(prefix="/api/v1", tags=["search"])


@router.post("/search", response_model=SearchResponse)
@limit_er.limit("3/day")
async def search_reddit_consensus(request: SearchRequest):
    try:
        search_service = SearchService(comment_depth=request.comment_depth)
        result = await search_service.search(
            user_query=request.query, max_results=request.max_results,

        )

        return result

    except HTTPException as e:
        raise e
    except Exception as e:
        msg = str(e).lower()
        if "rate" in msg and "limit" in msg:
            raise RateLimitError()
        if "unavailable" in msg or "temporar" in msg:
            raise ServiceUnavailableError()
        if "bad gateway" in msg or "upstream" in msg:
            raise UpstreamError()
        raise InternalServerError()
