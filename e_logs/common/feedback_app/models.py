import textwrap

from django.db import models

from config.settings.settings_base import FEEDBACK_TG_BOT
from .services.telegram_bot import TelegramBot


class Feedback(models.Model):
    MESSAGE = textwrap.dedent(
        """
        <b>Пользователь</b>: {usr}
        <b>Почта</b>: {email}
        <b>Цех</b>: {plant}
        <b>Журнал</b>: {journal}
        <b>Тема</b>: {theme}
        <b>Cообщение</b>:
        {text}
        """
    )

    bot = TelegramBot(channel=FEEDBACK_TG_BOT["channel"],
                      token=FEEDBACK_TG_BOT["token"],
                      proxy_url=FEEDBACK_TG_BOT["url"])

    theme = models.CharField(max_length=200, verbose_name='Тема')
    text = models.CharField(max_length=1000, verbose_name='Сообщение')
    plant = models.CharField(max_length=50, verbose_name='Цех')
    journal = models.CharField(max_length=256, verbose_name="Журнал")
    email = models.CharField(max_length=200, verbose_name='Почта')
    username = models.CharField(max_length=200, blank=True, null=True, verbose_name='Пользователь')

    def send_feedback(self):
        msg = Feedback.MESSAGE.format(
            usr=self.username,
            email=self.email,
            plant=self.plant,
            journal=self.journal,
            theme=self.theme,
            text=self.text,
        )
        Feedback.bot.send_message(msg)
        return self
