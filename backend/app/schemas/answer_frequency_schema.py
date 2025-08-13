from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, Optional
class FrequencyOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    reasoning: Optional[str] = Field(default="", description="How it calculated metrics")
    like_count: Dict[str, int] = Field(description="The sum of upvotes across all posts for the each of most popular answers")
    answer_frequency: Dict[str, int] = Field(description="The total number of mentions across all posts for each of the most popular answers")