import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.settings")

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