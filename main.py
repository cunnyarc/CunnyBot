"""
 ╔════════════════════════════════════════════════════════════════════════════════════════════════════════[─]═[□]═[×]═╗
 ║ MoeBot                                                                                                             ║
 ╠══════════════════════════╦═════════════════════════════════════════════════════════════════════════════════════════╣
 ║ Author:                  ║ https://github.com/GlitchChan                                                           ║
 ╠══════════════════════════╩═════════════════════════════════════════════════════════════════════════════════════════╣
 ║                                                                                                                    ║
 ║ This bot is quite simple and just grabs a random image from a list of subreddits and then posts them to both       ║
 ║  Discord and Twitter                                                                                               ║
 ║                                                                                                                    ║
 ║                                                                                                                    ║
 ╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
"""
import uuid
import tweepy
import random
import aiohttp
import asyncio
import logging
import mimetypes
import asyncprawcore.exceptions

from config import *
from secrets import *
from io import BytesIO
from asyncpraw import Reddit
from rich.logging import RichHandler
from asyncpraw.models import Submission, Subreddit
from discord_webhook import DiscordEmbed, AsyncDiscordWebhook
from apscheduler.schedulers.asyncio import AsyncIOScheduler

log: logging.Logger = logging.getLogger()
handler = RichHandler(rich_tracebacks=True, tracebacks_show_locals=True, log_time_format="%x %H:%M:%S.%f")
log.addHandler(handler)
log.setLevel(DEBUG if DEBUG else logging.INFO)
log.debug(f"Debug mod is {DEBUG}; This is not a warning just a reminder.")


async def get_reddit_post(subreddit: str) -> Submission:
    """
    Simple function to get a random post from a given subreddit

    :param subreddit: Subreddit to get post from
    :returns: A praw Submission
    """
    log.info(f"Getting submission from subreddit: {subreddit}")

    async with Reddit(
        client_id=REDDIT_ID,
        client_secret=REDDIT_SECRET,
        user_agent="Moebot by u/Glitchy_Red"
    ) as r:
        try:
            sub: Subreddit = await r.subreddit(subreddit)
            posts = [
                submission
                async for submission in sub.hot(limit=30)
                if not submission.is_self and not submission.url.startswith("https://v.redd.it/")
            ]
        except asyncprawcore.exceptions.ResponseException as e:
            log.warning(f"Reddit gave a {e.response.status}")

    post: Submission = random.choice(posts)
    return post


async def post_tweet(post: Submission) -> None:
    """
    Function to post submission to Twitter: https://twitter.com/CuteMoeBot

    :param post: Submission that will be tweeted
    """
    auth = tweepy.OAuth1UserHandler(
        TWITTER_CONSUMER_KEY,
        TWITTER_CONSUMER_SECRET,
        TWITTER_ACCESS_TOKEN,
        TWITTER_ACCESS_TOKEN_SECRET
    )
    twit = tweepy.API(auth)

    log.info("Getting image from post for Twitter")
    async with aiohttp.ClientSession() as ses:
        req = await ses.get(post.url)
        if req.status < 400:
            image = BytesIO(await req.content.read())
            image.seek(0)
            file_extension = mimetypes.guess_extension(req.headers['content-type'])
            image.name = f"{uuid.uuid4()}{file_extension}"
            log.debug(f"Succesfully got image: {image.name}")

    log.debug("Uploading Image to Twitter")
    media = twit.media_upload(filename=image.name, file=image)

    try:
        twit.update_status(status=post.title, media_ids=[media.media_id])
        log.info("Successfully Posted to Twitter")
    except tweepy.errors.TweepyException as e:
        log.exception(f"Failed to post to Twitter")


async def post_to_discord(post: Submission) -> None:
    """
    Function to post submission to discord: https://discord.gg/ZxbYHEh

    :param post: Submission that will be sent to webhook
    """
    log.debug("Creating Discord Webhook")
    webhook = AsyncDiscordWebhook(url=DISCORD_WEBHOOK_URL, rate_limit_retry=True)
    emb = DiscordEmbed(color=0xbc25cf, title=post.title)
    emb.set_image(url=post.url)
    webhook.add_embed(emb)
    try:
        await webhook.execute()
        log.info("Posted to Discord")
    except Exception:
        log.exception(f"Something happened when trying to post to discord")


async def run() -> None:
    """
    Main loop of the bot
    """
    subreddit = random.choice(SUBREDDITS)
    post = await get_reddit_post(subreddit)
    await asyncio.gather(
        post_tweet(post),
        post_to_discord(post)
    )

if __name__ == "__main__":
    sched = AsyncIOScheduler()
    sched.configure(timezone='America/New_York')
    sched.add_job(run, trigger="cron", hour="*", name="MoeBot")
    sched.start()
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
