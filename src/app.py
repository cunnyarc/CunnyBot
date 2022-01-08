import requests
import tempfile
import time
import sys

import schedule
import clients
from secrets import *
from colorama import Fore, Style

# Setup for all the clients
webhook = clients.DiscordWebhook(DISCORD_WEBHOOK_ID, DISCORD_WEBHOOK_TOKEN)
twitter = clients.TwitterClient(
    consumer_key=TWITTER_CONSUMER_KEY,
    consumer_secret=TWITTER_CONSUMER_SECRET,
    access_token=TWITTER_ACCESS_TOKEN,
    access_token_secret=TWITTER_ACCESS_TOKEN_SECRET
)
reddit = clients.RedditClient(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET)


def main():
    print(f"{Fore.YELLOW} Starting main loop...{Style.RESET_ALL}")
    post = reddit.get_post()
    image = requests.get(post['image'], stream=True)

    with tempfile.NamedTemporaryFile(mode="wb", suffix=".png") as moe:
        for chunk in image:
            moe.write(chunk)

        webhook.post_embed(image=post['image'], stats=post)
        twitter.tweet(image=moe, stats=post)


schedule.every().hour.do(main)

if __name__ == "__main__":
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}Received keyboard interrupt exiting...{Style.RESET_ALL}")
        sys.exit(0)
