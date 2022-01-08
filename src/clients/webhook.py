from discord import Embed, Webhook, RequestsWebhookAdapter, errors
from colorama import Fore, Style


class DiscordWebhook:
    def __init__(self, webhook_id, webhook_token):
        self.id = webhook_id
        self.token = webhook_token
        self.webhook = Webhook.partial(webhook_id,
                                       webhook_token,
                                       adapter=RequestsWebhookAdapter()
                                       )

    def post_embed(self, image, stats):
        embed = Embed(color=0xbc25cf)
        embed.set_author(name=stats['name'], url=stats['link'], icon_url=stats['author_image'])
        embed.set_image(url=image)

        try:
            self.webhook.send(embed=embed)
            print(f"{Fore.GREEN}{Style.BRIGHT}\u2714 Successfully posted image to Discord! {Style.RESET_ALL}")
        except errors.DiscordException:
            print(f"{Fore.RED}{Style.BRIGHT}\u274c A tweepy error occurred!{Style.RESET_ALL}")
            return
