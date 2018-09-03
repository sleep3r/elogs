import os
import django
from celery import Celery

os.environ['DJANGO_SETTINGS_MODULE'] = "config.settings.settings"
django.setup()

app = Celery('main', broker="redis://localhost:6379")

app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='Europe/Moscow',
)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))