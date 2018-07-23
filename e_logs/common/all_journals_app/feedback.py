import telepot
from e_logs.common.all_journals_app.models import Feedback

TOKEN = "484527904:AAHVkzp5hHuxWVfR0tYkIFPV-sgQkXQKqAQ"
CHANNEL = "-1001169474805"
CHANNEL_NAME = "@zxcvbnmasdfghjqwertyui"
MESSAGE = \
'''
<b>Пользователь</b>: {usr}
<b>Почта</b>: {email}
<b>Цех</b>: {plant}
<b>Журнал</b>: {journal}
<b>Тема</b>: {theme}
<b>Cообщение</b>:
{text}
'''

url="http://185.93.3.123:8080"

telepot.api.set_proxy(url)

Bot = telepot.Bot(TOKEN)


def send_feedback(data):
    Feedback(
        username=data["user"],
        email=data["email"],
        plant=data["plant"],
        journal=data["journal"],
        theme=data["theme"],
        text=data["text"]
    ).save()

    Bot.sendMessage(
        CHANNEL,
        MESSAGE.format(
            usr=data["user"],
            email=data["email"],
            plant=data["plant"],
            journal=data["journal"],
            theme=data["theme"],
            text=data["text"],
        ),
        parse_mode="HTML",
        disable_web_page_preview=True
    )
