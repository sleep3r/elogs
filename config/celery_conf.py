import os

from config import settings_setup

from celery import Celery

if os.environ.get('DOCKER') == 'yes':
    app = Celery('main', broker="redis://redis:6379")
else:
    app = Celery('main', broker="redis://localhost:6379")

app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='Europe/Moscow',  # TODO: take from settings
)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
