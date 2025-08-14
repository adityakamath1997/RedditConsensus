import praw
from dotenv import load_dotenv
import os
import asyncio


class RedditClient:
    def __init__(self, comment_depth: int):
        self.client = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT"),
        )

        self.comment_depth = comment_depth
        self._last_valid_posts = []

    async def get_posts_content(self, reddit_url_list: list[str]):
        loop = asyncio.get_event_loop()

        tasks = [
            loop.run_in_executor(None, self._extract_single_post_details, url)
            for url in reddit_url_list
        ]

        all_post_content = await asyncio.gather(*tasks, return_exceptions=True)
        valid_posts = [
            post
            for post in all_post_content
            if post is not None and not isinstance(post, Exception)
        ]
        self._last_valid_posts = valid_posts
        return self._format_post_content(valid_posts)

    def _format_post_content(self, posts_data):
        formatted_posts = []

        for i, post in enumerate(posts_data, 1):

            formatted_post = f"""POST {i}:
Title: {post['post_title']}
Author: {post['author']}
Content: {post['post_body']}

Top Comments:
"""

            for j, comment in enumerate(post["top_comments"], 1):
                formatted_post += (
                    f"{j}. ({comment['score']} upvotes) {comment['body']}\n"
                )

            formatted_posts.append(formatted_post)

        return formatted_posts

    def get_comments_and_upvotes(self):
        comments_and_upvotes= []
        for post in self._last_valid_posts:
            for comment in post.get("top_comments", []):
                comments_and_upvotes.append((comment.get("body", ""), int(comment.get("score", 0))))
        return comments_and_upvotes

    def _extract_single_post_details(self, url):
        try:
            submission = self.client.submission(url=url)

            submission.comments.replace_more(limit=0)
            sorted_comments = sorted(
                submission.comments, key=lambda c: c.score, reverse=True
            )[
                :self.comment_depth
            ]

            post_comment_details = []
            for top_comment in sorted_comments:
                comment_details = {
                    "body": top_comment.body,
                    "score": top_comment.score,
                }
                post_comment_details.append(comment_details)

            post_details = {
                "author": str(submission.author),
                "post_title": submission.title,
                "post_body": submission.selftext,
                "parent_comment_count": len(sorted_comments),
                "top_comments": post_comment_details,
            }

            print(f"Post details for {url} retrieved")

            return post_details

        except Exception as e:
            print(f"Exception occurred!: {e}")
            return None
