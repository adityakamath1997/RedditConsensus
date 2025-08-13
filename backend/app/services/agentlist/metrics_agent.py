from agents import Agent, Runner
from backend.app.schemas.answer_frequency_schema import FrequencyOutput
import asyncio

class MetricsAgent:
    def __init__(self, original_query):
        self.original_query = original_query
        self.agent = Agent(
            name="Metrics Generator Agent",
            instructions=self._get_instructions(),
            model="o4-mini",
            handoff_description="Used to calculate metrics for popular answers from reddit post comments",
        )

    def _get_instructions(self):
        metrics_generation_instructions = f"""
You are a metrics generator agent. You will serve as a tool to another agent who will receive a user query,
and a number of reddit posts with comments. That agent will answer the user query with a consensus of the comments on the posts provided to it.

You will receive a copy of the post details, as well as the other agents analysis. Your job is to analyze the post details
as well as the agent's output and find the 3-5 most popular answers. For each of these answers, you have two tasks:

1. Find the total number of mentions of each of these answers across all the post comments that are trying to answer the user query.
One-shot example:
Input:

Original user query: Most popular movie series of the last 50 years.

Post 1: <details>  Comment 1: Star Wars, Comment 2: Lord of the Rings Comment 3: Star Wars. Post 2: <details> Comment 1: Lord of the Rings. Comment 2: Star Wars. Comment 3. Harry Potter

Agent analysis: Star wars seems to be the most popular movie, followed by lord of the rings.

Output:
"star wars": 3, "lord of the rings": 2, "harry potter": 3
2. Find the sum of the number of upvotes across all comments that mention the most popular answers.

One-shot example:

Input:
Original user query: Most popular dog breeds
Post 1: <details> (20 upvotes) Comment 1: Golden retrievers and german shepherds rock!  (15 upvotes) Comment 2: I love golden retrievers
Post 2: <details> (5 upvotes) Comment 1: I like golden retrievers and pomeranians 

Output:
"german shepherd": 40, "german shepherd": 20, "pomeranian": 5

# Important: If multiple popular answers are contained in a single comment, the score/mentions in either case will count towards every popular answer contained in the comment.

You will output two dictionaries:
1. A dictionary containing key-value pairs of the most popular answers and their total mentions across all comments across all posts
2. A dictionary containing key-value pairs of the most popular answers and their total upvote count across all comments across all posts.

Think step-by-step in your analysis.

Here is the original query:
{self.original_query}
"""
        return metrics_generation_instructions

