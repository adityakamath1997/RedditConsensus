from pydantic import BaseModel, Field
from datetime import date

class QueryRewriteOutput(BaseModel):
    queries: list[str] = Field(description="Rewritten queries")
    start_date: str | None = Field(description="Start date in YYYY-MM-DD format")
    end_date: str | None = Field(description="End date in YYYY-MM-DD format")

