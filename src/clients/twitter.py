import tweepy

from tweepy.errors import TweepyException
from colorama import Fore, Style


class TwitterClient:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(self.auth)

    def tweet(self, image, stats):
        try:
            self.api.update_status_with_media(
                filename=image.name,
                status=f"{stats['name']} \n 🔗{stats['link']}"
            )
            print(f"{Fore.GREEN}{Style.BRIGHT}\u2714 Successfully posted to Twitter! {Style.RESET_ALL}")
        except TweepyException:
            print(f"{Fore.RED}{Style.BRIGHT}\u274c A tweepy error occurred!{Style.RESET_ALL}")
            return
