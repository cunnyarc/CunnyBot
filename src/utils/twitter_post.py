import logging
import tweepy

from tweepy.errors import TweepyException

# Setup logger
logger = logging.getLogger('moebot.twitter')


async def tweet_image(
        consumer_key: str,
        consumer_secret: str,
        access_token: str,
        access_token_secret: str,
        image_location: str,
        info: dict
) -> None:
    """Accesses the Twitter api to then tweet out the image with the submission info.

    :param consumer_key: Twitter developer consumer key.
    :param consumer_secret: Twitter developer consumer secret.
    :param access_token: Twitter auth access token.
    :param access_token_secret: Twitter auth access secret.
    :param image_location: Os path to image you want to upload.
    :param info: Information about the submission given.
    """

    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        api = tweepy.API(auth)

        api.update_status_with_media(
            filename=image_location,
            status=f"{info['name']} \n 🔗{info['link']}"
        )
        logger.info("Successfully tweeted to Twitter.")
    except TweepyException as e:
        logging.error(f"A tweepy exception was raised: `{e}`")
