import telepot
import telepot.namedtuple


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

    def send_media(self, files):
        media = [telepot.namedtuple.InputMediaPhoto(media=file) for file in files]
        self._bot.sendMediaGroup(
            self.channel,
            media,
        )
