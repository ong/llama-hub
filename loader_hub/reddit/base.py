"""Simple Reader that loads text relevant to a certain search keyword from subreddits"""
from typing import Any, List, Optional

from gpt_index.readers.base import BaseReader
from gpt_index.readers.schema.base import Document

class RedditReader(BaseReader):
    """
    Subreddit post and top-level comments reader for Reddit
    """

    def load_data(self, subreddits: List[str], search_keys: List[str], post_limit: Optional[int] = [10]) -> List[Document]:
        """
        Load text from relevant posts and top-level comments in subreddit(s), given keyword(s) for search

        Args:
            subreddits (List[str]): List of subreddits you'd like to read from
            search_keys (List[str]): List of keywords you'd like to use to search from subreddit(s)
            post_limit (Optional[int]): Maximum number of posts per subreddit you'd like to read from, defaults to 10
    
        """
        
        import praw
        import os
        from praw.models import MoreComments

        reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT'),
            username=os.getenv('REDDIT_USERNAME'),
            password=os.getenv('REDDIT_PASSWORD')
        )

        posts = []

        for sr in subreddits:
            ml_subreddit = reddit.subreddit(sr)

            for kw in search_keys:
                relevant_posts = ml_subreddit.search(kw, limit = post_limit)

                for post in relevant_posts:
                    posts.append(Document(post.selftext))
                    for top_level_comment in post.comments:
                        if isinstance(top_level_comment, MoreComments):
                            continue
                        posts.append(Document(top_level_comment.body))

        return posts
