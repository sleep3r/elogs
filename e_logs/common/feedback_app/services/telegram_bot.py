import telepot


class TelegramBot:
    def __init__(self, channel, token, proxy_url):
        telepot.api.set_proxy(proxy_url)
        self._bot = telepot.Bot(token)
        self.channel = channel

    def send_message(self, message):
        self._bot.sendMessage(
            self.channel,
            message,
            parse_mode="HTML",
            disable_web_page_preview=True
        )
