from pydantic import BaseModel, Field
from datetime import date

class QueryRewriteOutput(BaseModel):
    queries: list[str] = Field("Rewritten queries")
    start_date: str | None = Field("Start date in YYYY-MM-DD format")
    end_date: str | None = Field("End date in YYYY-MM-DD format")

