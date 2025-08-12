from pydantic import BaseModel, Field

class ConsensusAdditionalInfo(BaseModel):
    reasons: list[str] = Field("A list of 3 reasons why the consensus was arrived at")
    caveats: list[str] | None = Field("A list of caveats and warnings, like small number of posts/few comments")

class ConsensusOutput(BaseModel):
    consensus: str = Field("The answer to the users query, gathered from a consensus of reddit comments on relevant posts")
    additional_info: ConsensusAdditionalInfo = Field("Additional info including reasoning and caveats")

