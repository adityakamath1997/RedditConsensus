from pydantic import BaseModel, Field
from backend.app.schemas.answer_frequency_schema import FrequencyOutput

class ConsensusAdditionalInfo(BaseModel):
    reasons: list[str] = Field(
        description="A list of 3 reasons why the consensus was arrived at"
    )
    caveats: list[str] | None = Field(
        description="A list of caveats and warnings, like small number of posts/few comments"
    )


class ConsensusOutput(BaseModel):
    consensus: str = Field(
        description="The answer to the users query, gathered from a consensus of reddit comments on relevant posts"
    )
    additional_info: ConsensusAdditionalInfo = Field(
        description="Additional info including reasoning and caveats"
    )
    metrics: FrequencyOutput = Field("The metrics received from the analyse_metrics tool")
