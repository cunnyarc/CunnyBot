import aiohttp
import logging

from discord import Embed, Webhook, AsyncWebhookAdapter
from discord.errors import DiscordException

# Setup logger
logger = logging.getLogger('moebot.discord')


async def post_webhook(webhook_url: str, session: aiohttp.ClientSession, info: dict) -> None:
    """Posts submission image and information to the given webhook url.

    :param webhook_url: Discord Webhook url you want to send to
    :param session: aiohttp session to use to send the webhook
    :param info: utils submission info
    :return:
    """
    moe_embed = Embed(color=0xbc25cf).set_author(
        name=info['name'], url=info['link']
    ).set_image(
        url=info['image']
    )
    try:
        webhook = Webhook.from_url(webhook_url, adapter=AsyncWebhookAdapter(session))

        await webhook.send(embed=moe_embed)
        logger.info("Successfully send embed to Webhook.")

    except DiscordException as e:
        logger.error("A discord exception was raised: `{e}`")
