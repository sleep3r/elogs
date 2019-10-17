import os

import environ

from config import settings_setup

from celery import Celery

env = environ.Env(DEBUG=(bool, False))

app = Celery('main', broker=env("REDIS_URL"))

env = environ.Env(DEBUG=(bool, False))

app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone=env("TIMEZONE"),  # TODO: take from settings
)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
