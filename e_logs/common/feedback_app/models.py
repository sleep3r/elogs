import textwrap

from django.db import models

from django.conf import settings
from e_logs.core.utils.webutils import StrAsDictMixin
from e_logs.core.utils.loggers import err_logger
from .services.telegram_bot import TelegramBot
from .services.email import Email, EmailConnection

import os
import smtplib


class Feedback(StrAsDictMixin, models.Model):
    MESSAGE = textwrap.dedent(
        """
        <b>Пользователь</b>: {usr}
        <b>Почта</b>: {email}
        <b>Цех</b>: {plant}
        <b>Путь</b>: {url}
        <b>Тема</b>: {theme}
        <b>Cообщение</b>:
        {text}
        """
    )


    bot = TelegramBot(channel=settings.FEEDBACK_TG_BOT["channel"],
                      token=settings.FEEDBACK_TG_BOT["token"],
                      proxy=settings.FEEDBACK_TG_BOT["proxy"])


    theme = models.CharField(max_length=200, verbose_name='Тема', null=True, blank=True)
    text = models.CharField(max_length=1000, verbose_name='Сообщение', null=True, blank=True)
    plant = models.CharField(max_length=50, verbose_name='Цех', null=True, blank=True)
    url = models.CharField(max_length=256, verbose_name="URL", null=True, blank=True)
    email = models.CharField(max_length=200, verbose_name='Почта', null=True, blank=True)
    filenames = models.TextField(verbose_name="Имена файлов", default="")
    username = models.CharField(max_length=200, blank=True, null=True, verbose_name='Пользователь')

    @property
    def message(self):
        return Feedback.MESSAGE.format(
            usr=self.username,
            email=self.email,
            plant=self.plant,
            url=self.url,
            theme=self.theme,
            text=self.text,
        )


    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def send_feedback(self):
        self._send_telegram()
        self._send_mail()


    def _send_telegram(self):
        Feedback.bot.send_message(self.message)
        if self.filenames:
            Feedback.bot.send_media(self.filenames.split(','))
        return self
    
    def _send_mail(self):
        message = self.message.replace('\n', '<br/>')
        to_mail = settings.FEEDBACK_MAIL["to"]
        from_mail = settings.FEEDBACK_MAIL["mail"]
        password = settings.FEEDBACK_MAIL["password"]
        subject = "Kazzinc Elog Feedback"
        print(self.filenames)
        email = Email(from_mail, to_mail, subject, message, 
            message_type='html', attachments=self.filenames.split(','),
            message_encoding="utf-8",
        )
        conn = EmailConnection('smtp.gmail.com:465', to_mail, password)
        try:
            conn.send(email)
        except Exception as e:
            err_logger.critical("Почта накрылась!", e)