import asyncio
import sys
from distutils.util import strtobool
from io import BytesIO
from os import getenv
from pathlib import Path

from discord_webhook import AsyncDiscordWebhook
from dotenv import load_dotenv
from httpx import AsyncClient
from loguru import logger as log
from pygelbooru import Gelbooru
from pygelbooru.gelbooru import GelbooruImage
from tweepy import API, OAuth1UserHandler

# Load environment variables
load_dotenv()

# Setup more custom loguru logger
log.remove()
log.add(
    f"{Path(__file__).parent.absolute()}/logs/moebot.log",
    backtrace=True,
    enqueue=True,
    diagnose=True,
    rotation="00:00",
    retention="5 days",
)
log.add(sink=sys.stdout, level="DEBUG" if strtobool(getenv("DEBUG")) else "INFO", enqueue=True, colorize=True)
gel = Gelbooru(getenv("GELBOORU_API_KEY"), getenv("GELBOORU_USER_ID"))
webhook = AsyncDiscordWebhook(url=getenv("WEBHOOK"), rate_limit_retry=True)
auth = OAuth1UserHandler(
    getenv("TWITTER_CONSUMER_KEY"),
    getenv("TWITTER_CONSUMER_SECRET"),
    getenv("TWITTER_ACCESS_TOKEN"),
    getenv("TWITTER_ACCESS_TOKEN_SECRET"),
)
twit = API(auth)

# Configure what tags you want
TAGS = []

# Configure what tags to exclude
EXCLUDE_TAGS = [
    "1boy",
    "multiple_boys",
    "furry",
    "irl",
    "cosplay",
    "comic",
    "meme",
    "no_humans",
    "digimon",
    "bishoujo_senshi_sailor_moon",
    "adventure_time",
    "horror",
    "original",
    "non-web_source",
    "kirby_(series)",
    "pokemon",
    "rating:explicit",
    "my_little_pony",
    "rating:questionable",
    "feet",
    "senran_kagura",
    "monochrome",
    "very_dark_skin",
    "user:kamatamaudon",
    "translation_request",
    "third-party_edit",
]


@log.catch()
async def download_image(post: "GelbooruImage") -> "BytesIO":
    log.debug("Downloading Gelbooru image for Twitter")
    async with AsyncClient() as client:
        res = await client.get(post.file_url)
        image = BytesIO(res.content)
        image.name = f"{post.hash}.{post.file_url.split('.')[-1]}"
        image.seek(0)
        log.debug(f"Successfully Downloaded image as: {image.name}")
        return image


@log.catch()
async def post_discord(image: "GelbooruImage") -> None:
    log.info("Posting to Discord")
    webhook.content = image.file_url
    await webhook.execute()
    log.success("Successfully posted to Discord")


async def post_twitter(image: "BytesIO") -> None:
    log.info("Posting to Twitter")
    media = twit.media_upload(image.name, file=image)
    twit.update_status(status="", media_ids=[media.media_id])
    log.success("Sucessfully posted to Twitter")


@log.catch()
async def main() -> None:
    """Function to start script"""
    log.info("Starting script...")
    post: GelbooruImage = await gel.random_post(tags=TAGS, exclude_tags=EXCLUDE_TAGS)
    log.info("Found Gelbooru image to post")
    log.debug(f"Fetched gelbooru image: {post.file_url}")
    image = await download_image(post)
    await asyncio.gather(post_twitter(image), post_discord(post))
    log.success("Successfully completed script")


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
