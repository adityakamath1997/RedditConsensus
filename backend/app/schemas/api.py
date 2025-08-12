from pydantic import BaseModel, Field
from typing import Optional, List

class SearchRequest(BaseModel):
    query: str = Field(description="User's search query")
    max_results: int = Field(5, description="Max number of search results per reworded query", ge=1, le=20)

class AdditionalInfo(BaseModel):
    reasons: List[str] = Field(description="List of reasons supporting the consensus")
    caveats: List[str] = Field(description="List of warnings or limitations about the information")

class ConsensusData(BaseModel):
    consensus: str = Field(description="The main consensus answer from Reddit users")
    additional_info: AdditionalInfo = Field(description="Supporting reasons and caveats")

class SearchResponse(BaseModel):
    original_query: str = Field(description="The user's original search query")
    start_date: Optional[str] = Field(None, description="Start date filter (YYYY-MM-DD format)")
    end_date: Optional[str] = Field(None, description="End date filter (YYYY-MM-DD format)")
    posts_analyzed: int = Field(description="Number of Reddit posts successfully analyzed")
    consensus: ConsensusData = Field(description="The consensus analysis from Reddit posts")

