from pydantic import BaseModel, Field
from typing import Optional, List
from backend.app.schemas.answer_frequency_schema import FrequencyOutput

class SearchRequest(BaseModel):
    query: str = Field(description="User's search query")
    max_results: int = Field(
        5, description="Max number of search results per reworded query", ge=1, le=20
    )


class AdditionalInfo(BaseModel):
    reasons: List[str] = Field(description="List of reasons supporting the consensus")
    caveats: List[str] = Field(
        description="List of warnings or limitations about the information"
    )


class ConsensusData(BaseModel):
    consensus: str = Field(description="The main consensus answer from Reddit users")
    additional_info: AdditionalInfo = Field(
        description="Supporting reasons and caveats"
    )

class SearchResponse(BaseModel):
    original_query: str = Field(description="The user's original search query")
    start_date: Optional[str] = Field(
        None, description="Start date filter (YYYY-MM-DD format)"
    )
    end_date: Optional[str] = Field(
        None, description="End date filter (YYYY-MM-DD format)"
    )
    posts_analyzed: int = Field(
        description="Number of Reddit posts successfully analyzed"
    )
    reddit_urls: List[str] = Field(
        description="List of Reddit post URLs that were analyzed"
    )
    consensus: ConsensusData = Field(
        description="The consensus analysis from Reddit posts"
    )
    metrics: FrequencyOutput = Field(
        description="The frequency and score metrics"
    )
    answer_frequency_png: Optional[str] = Field(
        default=None,
        description="Base64 PNG of the Answer Frequency histogram",
    )
    like_count_png: Optional[str] = Field(
        default=None,
        description="Base64 PNG of the Total Upvotes histogram",
    )
