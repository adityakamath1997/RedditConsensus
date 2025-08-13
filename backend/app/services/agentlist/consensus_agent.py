from agents import Agent, Runner, ModelSettings
from backend.app.schemas.consensus_schema import ConsensusOutput
import asyncio


class ConsensusAgent:
    def __init__(self, original_query, post_details):
        self.original_query = original_query
        self.post_details = post_details
        self.agent = Agent(
            name="Consensus Generator",
            instructions=self._get_instructions(),
            model="gpt-4.1-mini",
            model_settings=ModelSettings(temperature=0.7),
            output_type=ConsensusOutput,
        )


    def _get_instructions(self):
        consensus_finder_instructions = """
You are a helpful assistant that will answer a user query from relevant reddit posts. You will be details of several relevant reddit posts.
Each posts details will be preceded by a post number (eg. POST 1) and the details will be structured in the following manner:
1. Post title
2. Post description
3. A list of the top 20 parent comments, sorted in descending order of their number of upvotes.

Your goal is to get a consensus of the comments in the posts provided and try and answer the users original query.

Take into consideration the following factors while arriving at a consensus:
1. How relevant is the post body to the users question
2. The helpful top comments and the number of upvotes they have.
3. Filter out any comments that seem like satire/sarcasm/comedy or are generally unhelpful.

#Important: For comments, each post will be PREPENDED by its upvote count

In addition to what appears to be the single most popular answer, also list out and describe other commonly appearing answering.
If no single answer is the most popular, answer with the most commonly appearing answers.
# Important: Make sure to strike a balance between number of mentions across posts, as well as the upvote count of the comments to guide your reasoning.

Answer the users original question and make sure to mention that the answer is a consensus of what reddit users think.

In addition to your final answer, include the following additional information:
1. 2-3 Reasons to justify your answer, including metrics from the analyze_metrics tool where relevant
2. 0-3 Caveats/Warnings to the user who is looking at this information. Make sure this is only about the source of the information. Examples might be few relevant posts/comments, or if some of the information seems sponsored etc.


"""
        return consensus_finder_instructions
    
    
    async def get_consensus(self):
        query = f"Original Query: '{self.original_query}' Posts details: ```{self.post_details}```"
        response = await Runner.run(self.agent, query)
        return response.final_output

