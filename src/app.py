# import asyncio
# import asyncpraw
# import tweepy
#
# Setup for all the clients
# webhook = clients.DiscordWebhook(DISCORD_WEBHOOK_ID, DISCORD_WEBHOOK_TOKEN)
# twitter = clients.TwitterClient(
#     consumer_key=TWITTER_CONSUMER_KEY,
#     consumer_secret=TWITTER_CONSUMER_SECRET,
#     access_token=TWITTER_ACCESS_TOKEN,
#     access_token_secret=TWITTER_ACCESS_TOKEN_SECRET
# )
# reddit = clients.RedditClient(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET)

# async def main():
#     print(f"{Fore.YELLOW} Starting main loop...{Style.RESET_ALL}")
#     post = reddit.get_post()
#     image = requests.get(post['image'], stream=True)
#
#     async with tempfile.NamedTemporaryFile(mode="wb", suffix=".png") as moe:
#         for chunk in image:
#             moe.write(chunk)
#
#         await asyncio.gather(
#             webhook.post_embed(image=post['image'], stats=post),
#             twitter.tweet(image=moe, stats=post),
#         )
#
#
# schedule.every().hour.do(main)
#
# if __name__ == "__main__":
#     try:
#         while True:
#             schedule.run_pending()
#             time.sleep(1)
#     except KeyboardInterrupt:
#         print(f"{Fore.YELLOW}Received keyboard interrupt exiting...{Style.RESET_ALL}")
#         sys.exit(0)
import utils
import re
import asyncio
import aiohttp
import logging

from time import strftime
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tempfile import NamedTemporaryFile
from secrets import *

# Setup logger
logging.basicConfig(
    encoding='utf-8',
    datefmt="%d-%m-%y %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger('moebot')
handler = TimedRotatingFileHandler(
    filename=f'moebot-{strftime("%d-%m-%y")}.log',
    when="D",
    interval=1,
    backupCount=5,
    encoding='utf-8',
    delay=False
)
handler.setFormatter(fmt=Formatter("%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)s] %(message)s"))
logger.addHandler(handler)


async def main() -> None:
    """Main loop of the entire bot"""
    logger.info("Starting main loop...")

    # Avoid rate limiting
    retries = 0

    # Get valid image
    image_regex = "https?://\S+?/\S+?\.(?:jpg|jpeg|gif|png)"

    while True:
        # Limit to only 5 retires
        if retries >= 5:
            logging.error("Failed to retrieve submission in limited tries...")
            break

        submission = await utils.get_submission(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET)
        info = await utils.get_submission_info(submission=submission)

        # Make sure we are getting a url ending in jpg, peg, gif, or png
        if info['image'] and re.match(pattern=image_regex, string=info['image']):
            logging.info("Successfully retrieved submission")
            break

        logger.warning("Failed to get submission, retrying...")
        retries += 1

    # Create aiohttp session to get image for Twitter
    async with aiohttp.ClientSession() as session:
        async with session.get(info['image']) as resp:
            logging.info("Retrieving image for Twitter api...")
            with NamedTemporaryFile('wb', suffix=f"{info['image'][-3:]}") as moe:
                moe.write(await resp.read())

                logger.info("Posting to Discord and Twitter...")

                # Send out the gathered information to Twitter and Discord
                await asyncio.gather(
                    utils.post_webhook(DISCORD_WEBHOOK_URL, session, info),
                    utils.tweet_image(
                        TWITTER_CONSUMER_KEY,
                        TWITTER_CONSUMER_SECRET,
                        TWITTER_ACCESS_TOKEN,
                        TWITTER_ACCESS_TOKEN_SECRET,
                        moe.name,
                        info
                    )
                )

    logger.info("Successfully completed job.")

if __name__ == "__main__":
    # Setup scheduler for periodic jobs
    scheduler = AsyncIOScheduler()
    scheduler.configure(timezone='America/New_York')
    scheduler.add_job(main, trigger='cron', hour='*')
    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()

    except (KeyboardInterrupt, SystemExit):
        print("Killing...")
        pass
