from agents import Agent, Runner, ModelSettings
from app.schemas.relevance_schema import RelevanceOutput

class RelevanceCheckerAgent:
    def __init__(self, original_query):

        self.original_query = original_query
        self.agent = Agent(
            name="Relevancy checker agent",
            instructions=self._get_instructions(),
            model_settings=ModelSettings(temperature=0.7, max_tokens=500),
            model="gpt-4.1",
            output_type=RelevanceOutput
            
        )

    def _get_instructions(self):
        relevance_checker_instructions = """
        You are a reddit post relevance checker agent. 
        You will receive a user query, and a list of Reddit posts containing similar questions to the users question.
        Your job is to filter out the irrelevant posts, or the ones that don't align well the users question.
        You will output a list of boolean values, in respective order of the input posts, True if the post is quite similar to the users question,
        False if it isnt.

        Example:
        User query: Best crime dramas to watch on TV

        Reddit post 1: What are the best crime dramas on TV?
        Reddit post 2. Best true crime books
        Reddit post 3. Best crime documentaries
        Reddit post 4. Crime TV Suggestions?

        Output: [True, False, False, True]

        Reason: Post 2 and 3 are about books and documentaries respectively, they dont answer the user query.

        Output in the JSON schema specified.

"""
        return relevance_checker_instructions
    async def get_relevance(self, url_list):
        query = f"Original query: {self.original_query} Reddit URL list: {url_list}"
        response = await Runner.run(self.agent, query)
        return response.final_output.relevance_check

