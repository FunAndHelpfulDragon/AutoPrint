from discord_webhook import DiscordWebhook


class webhook:

    def __init__(self):
        with open("webhook.txt", 'r') as f:
            self.url = f.read().strip()

    def SendMessage(self, message):
        webhook = DiscordWebhook(url=self.url, content=message)
        response = webhook.execute()
        print(response)
