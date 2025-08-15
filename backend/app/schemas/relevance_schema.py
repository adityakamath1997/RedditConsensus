from pydantic import BaseModel, Field

class RelevanceOutput(BaseModel):
    relevance_check: list[bool] = Field(description="A relevance check on the list of reddit urls passed")