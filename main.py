"""
 ╔════════════════════════════════════════════════════════════════════════════════════════════════════════[─]═[□]═[×]═╗
 ║ MoeBot                                                                                                             ║
 ╠══════════════════════════╦═════════════════════════════════════════════════════════════════════════════════════════╣
 ║ Author:                  ║ https://github.com/GlitchChan                                                           ║
 ╠══════════════════════════╩═════════════════════════════════════════════════════════════════════════════════════════╣
 ║                                                                                                                    ║
 ║ This bot is quite simple and just grabs a random image from a list of subreddits and then posts them to both       ║
 ║   Discord and Twitter                                                                                              ║
 ║                                                                                                                    ║
 ║                                                                                                                    ║
 ╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import random
import tempfile
import aiohttp
import tweepy

from secrets import *
from config import DEBUG, SUBREDDITS
from utils import logutils
from discord_webhook import DiscordEmbed, AsyncDiscordWebhook
from asyncpraw import Reddit
from asyncpraw.models import Submission
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logger = logutils.init_logger("moebot")
logger.info(f"Debug mod is {DEBUG}; This is not a warning just a reminder.")
auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
twitter = tweepy.API(auth)


async def reddit_post():
    """Fetch reddit post to send out"""
    logger.info("Getting post from reddit")

    async with Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent="post grabber"
    ) as reddit:
        while True:
            subreddit = await reddit.subreddit(random.choice(SUBREDDITS))
            posts = [submission async for submission in subreddit.hot(limit=30)]
            post = random.choice(posts)

            if post.url and not post.url.startswith("https://v.redd.it/"):
                return post


async def tweet(post: Submission):
    """Tweets out the reddit post"""
    async with aiohttp.ClientSession() as session:
        async with session.get(post.url) as resp:
            logger.info("Getting image for Twitter")

            with tempfile.NamedTemporaryFile('wb') as image:
                image.write(await resp.read())

                logger.debug(image.name)
                logger.info("Attempting to post to Twitter")
                try:
                    twitter.update_status_with_media(filename=image.name, status=post.title)
                    logger.info("Posted to twitter")
                except Exception:
                    logger.warning("Failed to post to Twitter, probably image issue", exc_info=DEBUG)


async def discord_webhook(post: Submission):
    """Sends the reddit post to discord"""
    logger.info("Sending Image to Discord")
    webhook = AsyncDiscordWebhook(url=DISCORD_WEBHOOK_URL, rate_limit_retry=True)
    emb = DiscordEmbed(color=0xbc25cf, title=post.title, url=post.shortlink)
    emb.set_image(url=post.url)
    webhook.add_embed(emb)
    await webhook.execute()


async def main():
    """
    Main loop of the bot

    Main
    |-Get Reddit post
        |- Post to Twitter
        |- Post to Discord
    Loop
    """
    logger.info("Starting main loop", exc_info=DEBUG)
    post = await reddit_post()
    await asyncio.gather(
        discord_webhook(post),
        tweet(post)
    )

if __name__ == "__main__":
    # Setup scheduler for periodic jobs
    scheduler = AsyncIOScheduler()
    scheduler.configure(timezone='America/New_York')
    scheduler.add_job(main, trigger='cron', hour='*')
    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()

    except (KeyboardInterrupt, SystemExit):
        logger.info("Shutting down main loop...")
