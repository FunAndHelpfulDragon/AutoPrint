from discord_webhook import DiscordWebhook


class webhook:

    def __init__(self, url):
        self.url = url

    def SendMessage(self, message):
        webhook = DiscordWebhook(url=self.url, content=message)
        response = webhook.execute()
        print(response)
