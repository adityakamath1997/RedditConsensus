from fastapi import APIRouter, HTTPException, Request
from app.services.search_service import SearchService
from app.schemas.api import SearchRequest, SearchResponse
from app.errors import RateLimitError, ServiceUnavailableError, UpstreamError, InternalServerError
from app.core.limiter import limiter
from app.services.agentlist.relevance_checker_agent import RelevanceCheckerAgent
from app.services.agentlist.consensus_agent import ConsensusAgent
from app.services.agentlist.metrics_agent import MetricsAgent
from app.services.plot_service import build_histogram_images
import asyncio
import json
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/api/v1", tags=["search"])


@router.post("/search", response_model=SearchResponse)
@limiter.limit("5/day")
async def search_reddit_consensus(request: Request, payload: SearchRequest):
    try:
        search_service = SearchService(comment_depth=payload.comment_depth)
        result = await search_service.search(
            user_query=payload.query, max_results=payload.max_results,

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


@router.get("/search/stream")
@limiter.limit("5/day")
async def search_reddit_consensus_stream(request: Request, query: str, max_results: int = 5, comment_depth: int = 10):
    def to_dict(obj):
        if hasattr(obj, "model_dump"):
            return obj.model_dump()
        if hasattr(obj, "dict"):
            return obj.dict()
        return obj

    async def sse_event(event_name: str, data_obj) -> str:
        return f"event: {event_name}\ndata: {json.dumps(data_obj)}\n\n"

    async def event_generator():
        try:
            service = SearchService(comment_depth=comment_depth)

            # 1) Rewrite queries
            rewrite_result = await service.query_rewriter.rewrite_query(query)
            # Only emit non-sensitive summary stats (no prompts/post content)
            yield await sse_event("rewritten", {
                "num_queries": len(rewrite_result.queries or []),
                "start_date": rewrite_result.start_date,
                "end_date": rewrite_result.end_date,
            })

            # 2) Reddit search
            reddit_urls = await service.tavily_client.tavily_search(
                queries=rewrite_result.queries,
                max_results=max_results,
                start_date=rewrite_result.start_date,
                end_date=rewrite_result.end_date,
            )
            yield await sse_event("search_complete", {
                "total_urls": len(reddit_urls),
            })

            #3) Relevance filter
            original_query = rewrite_result.queries[0] if rewrite_result.queries else query
            relevancy_agent = RelevanceCheckerAgent(original_query=original_query)
            relevancy_check = await relevancy_agent.get_relevance(reddit_urls)
            relevant_reddit_urls = [url for url, flag in zip(reddit_urls, relevancy_check) if flag]
            yield await sse_event("urls_filtered", {
                "total": len(reddit_urls),
                "relevant": len(relevant_reddit_urls),
                "filtered": max(0, len(reddit_urls) - len(relevant_reddit_urls)),
            })

            # Fetch post content
            post_details = await service.reddit_client.get_posts_content(relevant_reddit_urls)

            # 4) Consensus and 5) Metrics in parallel, stream as they complete
            consensus_agent = ConsensusAgent(original_query=original_query, post_details=post_details, model=service.model)
            metrics_agent = MetricsAgent(original_query=original_query, post_details=post_details, model=service.model)

            consensus_task = asyncio.create_task(consensus_agent.get_consensus())
            metrics_task = asyncio.create_task(metrics_agent.get_metrics())

            done, pending = await asyncio.wait({consensus_task, metrics_task}, return_when=asyncio.FIRST_COMPLETED)
            for task in done:
                if task is consensus_task:
                    consensus = task.result()
                    yield await sse_event("consensus_generated", {"has_alternatives": bool(getattr(consensus, "additional_answers", []))})
                else:
                    metrics = task.result()
                    yield await sse_event("metrics_generated", {"answers": len(getattr(metrics, "answer_frequency", []))})

            # Await the remaining task and emitt its event
            if not consensus_task.done():
                consensus = await consensus_task
                yield await sse_event("consensus_generated", {"has_alternatives": bool(getattr(consensus, "additional_answers", []))})
            if not metrics_task.done():
                metrics = await metrics_task
                yield await sse_event("metrics_generated", {"answers": len(getattr(metrics, "answer_frequency", []))})

            # Build images 
            histogram_images = build_histogram_images(metrics, max_bars=15)
            final_payload = {
                "original_query": query,
                "start_date": rewrite_result.start_date,
                "end_date": rewrite_result.end_date,
                "posts_analyzed": len(post_details),
                "reddit_urls": relevant_reddit_urls,
                "consensus": to_dict(consensus),
                "metrics": to_dict(metrics),
                "answer_frequency_png": histogram_images.get("answer_frequency_png"),
                "like_count_png": histogram_images.get("like_count_png"),
            }
            yield await sse_event("done", final_payload)

        except Exception as e:
            # Send an error to client
            yield await sse_event("error", {"message": str(e)})

    headers = {"Cache-Control": "no-cache", "Connection": "keep-alive"}
    return StreamingResponse(event_generator(), media_type="text/event-stream", headers=headers)
