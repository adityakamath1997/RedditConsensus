from pydantic import BaseModel, Field
from typing import Dict, Union

class FrequencyOutput(BaseModel):
    like_count: Dict[str, int] = Field(description="The sum of upvotes across all posts for the each of most popular answers",
                                           json_schema_extra={"minItems": 3, "maxItems": 5})
    answer_frequency: Dict[str, int] = Field(description="The total number of mentions across all posts for each of the most popular answers",
                                             json_schema_extra={"minItems": 3, "maxItems": 5})