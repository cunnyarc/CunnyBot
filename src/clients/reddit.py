import random
import praw

from praw.exceptions import RedditAPIException
from colorama import Fore, Style

SOURCES = [
    "awwnime",
    "moescape",
    "onodera",
    "tsunderes",
    "hatsune",
    "TwoDeeArt",
    "Honkers",
    "thecutestidol",
    "LoveArrowShoot",
    "LegendaryMinalinsky",
    "TheRiceGoddess",
    "Harasho",
    "washiwashi",
    "onetrueidol",
    "MioFanClub",
    "TainakaRitsu",
    "azunyan",
    "onetruebiribiri",
    "saber",
    "headpats",
    "homura",
    "Sayaka",
    "animelegwear",
    "tyingherhairup",
    "cutelittlefangs",
    "Patchuu",
    "Megumin",
    "pouts",
    "megane"
]


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

    def _get_submission(self):
        subbreddit = random.choice(SOURCES)
        submissions = []

        for submission in self.reddit.subreddit(subbreddit).hot(limit=10):
            submissions.append(submission)

        submission = random.choice(submissions)

        return submission

    def get_post(self):
        try:
            submission = self._get_submission()
            stats = self._get_post_stats(submission)
        except RedditAPIException:
            print(f"{Fore.RED}{Style.BRIGHT}\u274c A praw error occurred!{Style.RESET_ALL}")
            return

        print(f"{Fore.GREEN}{Style.BRIGHT}\u2714 Successfully retrieved post! {Style.RESET_ALL}")
        return stats
