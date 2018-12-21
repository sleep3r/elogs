import telepot
import telepot.namedtuple
import telegram
from telegram.error import NetworkError, Unauthorized
from telegram.utils.request import Request


class TelegramBot:
    def __init__(self, channel, token, proxy):
        request = Request(proxy_url=proxy["url"],
                          urllib3_proxy_kwargs={
                            "username": proxy["username"],
                            "password": proxy["password"]
                          })
        self._bot = telegram.Bot(token=token, request=request)
        self.channel = channel

    def send_message(self, message):
        self._bot.sendMessage(
            self.channel,
            message,
            parse_mode="HTML",
            disable_web_page_preview=True)

    def send_media(self, files):
        media = [telegram.InputMediaPhoto(media=open(filepath, "rb")) for filepath in files]
        self._bot.sendMediaGroup(
            self.channel,
            media)
