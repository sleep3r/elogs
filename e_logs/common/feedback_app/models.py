import textwrap

from django.db import models

from django.conf import settings
from e_logs.core.utils.webutils import StrAsDictMixin
from .services.telegram_bot import TelegramBot


class Feedback(StrAsDictMixin, models.Model):
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

    bot = TelegramBot(channel=settings.FEEDBACK_TG_BOT["channel"],
                      token=settings.FEEDBACK_TG_BOT["token"],
                      proxy_url=settings.FEEDBACK_TG_BOT["url"])

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
