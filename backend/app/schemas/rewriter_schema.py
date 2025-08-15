from pydantic import BaseModel, Field


class QueryRewriteOutput(BaseModel):
    queries: list[str] = Field(description=" Original query plus 5 Rewritten queries")
    start_date: str | None = Field(description="Start date in YYYY-MM-DD format")
    end_date: str | None = Field(description="End date in YYYY-MM-DD format")
