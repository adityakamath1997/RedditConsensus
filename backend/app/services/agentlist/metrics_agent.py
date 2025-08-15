from agents import Agent, Runner, AgentOutputSchema, ModelSettings
from backend.app.schemas.answer_frequency_schema import FrequencyOutput

class MetricsAgent:
    def __init__(self, original_query, post_details, model):
        self.original_query = original_query
        self.post_details = post_details
        self.agent = Agent(
            name="Metrics Generator Agent",
            instructions=self._get_instructions(),
            model=model,
            model_settings=ModelSettings(temperature=0.3),
            output_type=AgentOutputSchema(FrequencyOutput, strict_json_schema=False)
        )

    def _get_instructions(self):
        metrics_generation_instructions = f"""
You are a metrics generator agent. Your job is to answer a user query by analyzing comments from Reddit posts that are likely to contain answers to the user's query.
You will receive a user query, followed by a list of Reddit posts (typically 10-20). Each post includes:

The post title
The post body
A list of the top comments (up to 25 parent comments), where each comment is preceded by its upvote score (e.g., "[Upvotes: 150] Comment text here").

Your task is to identify the 5-10 most popular distinct answers to the user query across all comments in all posts. Focus only on comments that appear to be attempting to answer the query, based on relevance to the user query and the post title/body.
Approach:

Identify and group answers: Read each comment independently. Extract potential answers from comments that address the query. Group similar or equivalent answers into distinct categories (e.g., if "Python" and "Use Python programming language" mean the same thing, treat them as one answer). Normalize phrasing to avoid duplicates while preserving meaning. Ignore off-topic comments, jokes, or non-answers.
Determine popularity: Rank answers by the total number of mentions (descending) to select the top 5-10. If there are ties, use total upvote score as a tiebreaker.
Tally metrics for each top answer:

Mentions count: For each distinct answer, count the total number of comments (across all posts) that mention it at least once. Each such comment counts as 1 mention for that answer, regardless of how many times it's repeated within the comment.

Important: If a single comment mentions multiple answers, count it as 1 mention toward each relevant answer.


Upvote score sum: For each distinct answer, sum the upvote scores of all comments that mention it at least once. Use only the upvote score provided for each comment.

Important: If a single comment mentions multiple answers, add its full upvote score to each relevant answer.





Think step-by-step in your analysis. Calculate metrics as accurately as possible by processing each comment one by one. Double-check for grouping accuracy and ensure no double-counting or omissions.

Output in the JSON schema specified.

"""
        return metrics_generation_instructions
    
    async def get_metrics(self):

        query = f"Original Query: '{self.original_query}' Posts details: ```{self.post_details}```"
        analysis = await Runner.run(self.agent, query)
        return analysis.final_output

