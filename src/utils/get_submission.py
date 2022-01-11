import os
import asyncpraw
import random
import logging

from aiofiles import open
from asyncpraw.models import Submission, Subreddit

last_used_subreddit = None

# Setup logger
logger = logging.getLogger('moebot.reddit')


async def _get_sources() -> list:
    """Gets the subreddit sources from sources.txt"""
    async with open(os.path.join("./sources.txt"), mode='r') as sources_list:
        sources = [source.strip(',\n') for source in await sources_list.readlines()]

    return sources


async def _get_subreddit(sources: list) -> Subreddit:
    """Gets a random subreddit and makes sure it not a repeat.

    :param sources: A list of sources to randomly choose from.
    :return: A Subreddit to get information from.
    """

    global last_used_subreddit

    while True:
        subreddit = random.choice(sources)

        if subreddit != last_used_subreddit:
            last_used_subreddit = subreddit
            return subreddit


async def get_submission_info(submission: Submission) -> dict:
    """ Gets information about the submission for later use

    :param submission: Submission to get information from.
    :return: A Dict of information about the Submission.
    """

    info = {
        "name": submission.title,
        "link": submission.shortlink,
        "image": submission.url,
    }

    return info


async def get_submission(client_id: str, client_secret: str) -> Submission:
    """Gets a random submission from a subreddit.

    :param client_id: Reddit api client ID
    :param client_secret: Reddit api client secret
    :return: An instance of asyncpraw Submission
    """

    sources = await _get_sources()
    subreddit_to_use = await _get_subreddit(sources)

    async with asyncpraw.Reddit(client_id=client_id, client_secret=client_secret, user_agent="Moe Bot") as reddit:
        subreddit = await reddit.subreddit(subreddit_to_use)
        submissions = []
        async for submission in subreddit.hot(limit=30):
            submissions.append(submission)

        submission = random.choice(submissions)

    return submission
