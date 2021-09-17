from discord_webhook import DiscordWebhook
import os


class webhook:

    def __init__(self):
        with open(f"{os.path.dirname(__file__)}/webhook.txt", 'r') as f:
            self.url = f.read().strip()

    def SendMessage(self, message):
        webhook = DiscordWebhook(url=self.url, content=message)
        response = webhook.execute()
        print(response)
