import uuid
import random
import asyncio
import logging
import mimetypes
import asyncprawcore
import requests
import tweepy.errors


from os import getenv
from io import BytesIO
from asyncpraw import Reddit
from logging import Formatter
from dotenv import load_dotenv
from aiohttp import ClientSession
from asyncpraw.models import Submission
from tweepy import OAuth1UserHandler, API
from discord_webhook import DiscordWebhook
from logging.handlers import TimedRotatingFileHandler


load_dotenv()
log = logging.getLogger('moebot')
handler = TimedRotatingFileHandler(filename='./logs/runtime.log', when='D', interval=1, backupCount=10, encoding='utf-8', delay=False)
formatter = Formatter(fmt="[%(asctime)s] - [%(levelname)-7s : %(lineno)d]: %(message)s")
handler.setFormatter(formatter)
log.addHandler(handler)

# Set logging level
log.setLevel(logging.INFO)


async def reddit_post(subreddit: str) -> Submission:
    """
    Function to get a random post from a given subreddit

    :param subreddit: Subreddit to take posts from
    :return: A PRAW Submission object
    """
    log.info(f"Getting a submission from the subreddit: {subreddit}")

    async with Reddit(
        client_id=getenv('REDDIT_ID'),
        client_secret=getenv('REDDIT_SECRET'),
        user_agent="MoeBot with AsyncPRAW"
    ) as r:
        try:
            sub = await r.subreddit(subreddit)
            post = random.choice([
                submission
                async for submission in sub.hot(limit=30)
                if not submission.is_self and not submission.url.startswith("https://v.redd.it/")
            ])
            log.debug(f"Got post {post.title}")
            return post
        except asyncprawcore.exceptions.ResponseException as e:
            log.exception(f'Reddit gave a {e.response.status}')


async def get_image(post: Submission) -> BytesIO:
    """
    Function to download an image from a reddit post

    :param post: PRAW Submission object
    :returns: BytesIO object
    """
    log.debug(f"Downloading image for post {post.id}")
    async with ClientSession() as ses:
        req = await ses.get(post.url)
        if req.status < 400:
            image = BytesIO(await req.content.read())
            file_extension = mimetypes.guess_extension(req.headers['content-type'])
            image.name = f"{uuid.uuid4()}{file_extension}"
            log.debug(f"Succesfully got image: {image.name}")
    return image


async def tweet(post: Submission, image: BytesIO) -> None:
    """
    Function to post given submission to Twitter Account

    :param post: PRAW Submission object
    :param image: BytesIO object to send to Twitter
    """
    auth = OAuth1UserHandler(
        getenv('TWITTER_CONSUMER_KEY'),
        getenv('TWITTER_CONSUMER_SECRET'),
        getenv('TWITTER_ACCESS_TOKEN'),
        getenv('TWITTER_ACCESS_TOKEN_SECRET')
    )
    t = API(auth)
    log.debug("Uploading image to Twitter")
    try:
        media = t.media_upload(filename=image.name, file=image)
        t.update_status(status=post.title, media_ids=[media.media_id])
        log.info("Posted to Twitter")
    except tweepy.errors.TweepyException as e:
        log.warning(f"Tweepy gave error {e.__class__}")


async def discord(post: Submission, image: BytesIO) -> None:
    """
    Function to post the given submission to Discord webhook

    :param post: PRAW Submission object
    :param image: BytesIO object to send to Discord
    """
    location = image.tell()
    image.seek(location)
    hook = DiscordWebhook(getenv('WEBHOOK'), rate_limit_retry=True, content=post.title)
    hook.add_file(image.getvalue(), image.name)
    try:
        hook.execute()
        log.info("Posted to Discord")
    except requests.exceptions.HTTPError as e:
        log.warning(f"Discord Webhook gave error {e.__class__}: {e.response}")


async def main() -> None:
    """Entry function to get the bot running"""
    log.info("Starting loop")
    subreddits = open('subreddits.txt', 'r').read().splitlines()
    subreddit = random.choice(subreddits)

    post = await reddit_post(subreddit)
    img = await get_image(post)

    await asyncio.gather(
        discord(post, img),
        tweet(post, img)
    )

if __name__ == '__main__':
    asyncio.run(main())
