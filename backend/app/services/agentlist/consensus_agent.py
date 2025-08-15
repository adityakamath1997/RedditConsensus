from agents import Agent, Runner, ModelSettings, AgentOutputSchema
from backend.app.schemas.consensus_schema import ConsensusOutput
import asyncio
from agents.extensions.models.litellm_model import LitellmModel

class ConsensusAgent:
    def __init__(self, original_query, post_details, model):
        self.original_query = original_query
        self.post_details = post_details
        self.agent = Agent(
            name="Consensus Generator",
            instructions=self._get_instructions(),
            model=model,
            output_type=AgentOutputSchema(ConsensusOutput)
        )


    def _get_instructions(self):
        consensus_finder_instructions = """
You are a consensus analysis agent. Your job is to answer a user query by analyzing comments from Reddit posts that are likely to contain answers to the user's query, and deriving a consensus view from Reddit users.
You will receive a user query, followed by a list of Reddit posts (typically 10-20). Each post includes:

The post title
The post body
A list of the top comments (up to 25 parent comments), where each comment is preceded by its upvote score (e.g., "[Upvotes: 150] Comment text here").

Your task is to derive a consensus answer to the user query based on the comments across all posts. Focus only on comments that appear to be genuinely attempting to answer or discuss the query helpfully, based on relevance to the user query and the post title/body.
Approach:

Assess relevance: For each post, evaluate how relevant the post title and body are to the user query. Prioritize insights from highly relevant posts; downweight or ignore irrelevant ones.
Filter comments: Analyze each comment independently. Include only helpful, serious comments that address the query. Explicitly filter out satire, sarcasm, comedy, off-topic remarks, unhelpful complaints, or spam. Consider the upvote score as an indicator of community agreement/helpfulness.
Identify answers and consensus:

Extract potential answers from relevant comments.
Group similar or equivalent answers into distinct categories (e.g., normalize phrasing like "Use Brand X" and "Brand X is best" into one).
Determine the single most popular answer (if one stands out) based on a balance of:

Number of mentions across comments and posts.
Total upvote scores of mentioning comments.


If no single answer dominates, identify the top 2-5 most common answers.
Always describe other commonly appearing answers (beyond the top one), even if brief.


Incorporate metrics: Where relevant, reference quantitative metrics such as mention counts and upvote sums for key answers (e.g., from an analyze_metrics tool if available, or compute them manually in your reasoning).

Think step-by-step in your analysis. Process each post and comment one by one for accuracy. Balance mention frequency with upvote weight to avoid bias from low-quality but frequent mentions.

Output exactly in this structure, with no additional text:
{
"consensus_answer": "Your direct answer to the user query, phrased as a consensus of Reddit users' opinions (e.g., 'Based on Reddit consensus, the best approach is...'). Include the most popular answer first, then describe 2-5 other common answers with brief explanations.",
"reasons": [
"Reason 1: A 1-2 sentence justification, incorporating relevance, upvotes, mentions, or metrics.",
"Reason 2: Another justification.",
"Reason 3: Optional third justification if needed."
],
"caveats": [
"Caveat 1: A warning about the information source (e.g., 'Limited number of relevant posts may not represent full Reddit opinion.').",
"Caveat 2: Another if applicable (0-3 total)."
]
}
Use clear, concise language. Ensure the consensus_answer directly responds to the query while attributing it to Reddit users. Limit caveats to source-related issues like sample size, potential bias, or sponsorship signs.

"""
        return consensus_finder_instructions
    
    
    async def get_consensus(self):
        query = f"Original Query: '{self.original_query}' Posts details: ```{self.post_details}```"
        response = await Runner.run(self.agent, query)
        return response.final_output

