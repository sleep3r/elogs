import os
import sys
import logging
from logging.handlers import TimedRotatingFileHandler

from django.core.management.color import color_style


class ColorsFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style = self.configure_style(color_style())

    @staticmethod
    def configure_style(style):
        style.DEBUG = style.HTTP_NOT_MODIFIED
        style.INFO = style.HTTP_REDIRECT
        style.WARNING = style.HTTP_NOT_FOUND
        style.CRITICAL = style.HTTP_SERVER_ERROR
        return style

    def format(self, record):
        message = logging.Formatter.format(self, record)
        if sys.version_info[0] < 3:
            message = message.encode('utf-8', errors='coerce')
        colorizer = getattr(self.style, record.levelname, self.style.HTTP_SUCCESS)
        # message = colorizer(message)
        return message


class MkdirTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename, when='h', interval=1, backupCount=0, encoding=None, delay=False,
                 utc=False, atTime=None):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        TimedRotatingFileHandler.__init__(self, filename, when, interval, backupCount, encoding, delay,
                                     utc, atTime)
