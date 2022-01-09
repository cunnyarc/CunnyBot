import random
import os

import praw
from praw.exceptions import RedditAPIException
from colorama import Fore, Style


class RedditClient:
    def __init__(self, client_id, client_secret):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent="MoeBot"
        )

    def _get_post_stats(self, submission):
        stats = {
            "name": submission.title,
            "link": submission.shortlink,
            "image": submission.url,
            "author_image": submission.author.icon_img
        }

        return stats

    def _get_sources(self):
        with open(os.path.join("./sources.txt"), 'r') as sources_list:
            sources = [source.strip(',\n') for source in sources_list.readlines()]

        return sources

    def _get_submission(self):
        sources = self._get_sources()
        subbreddit = random.choice(sources)

        submission = random.choice([submission for submission in self.reddit.subreddit(subbreddit).hot(limit=25)])

        return submission

    def get_post(self):
        try:
            submission = self._get_submission()
            stats = self._get_post_stats(submission)
            print(f"{Fore.GREEN}{Style.BRIGHT}\u2714 Successfully retrieved post! {Style.RESET_ALL}")
            return stats
        except RedditAPIException:
            print(f"{Fore.RED}{Style.BRIGHT}\u274c A praw error occurred!{Style.RESET_ALL}")
            pass
