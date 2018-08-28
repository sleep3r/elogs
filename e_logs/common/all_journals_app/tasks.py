import os
from celery import Celery

app = Celery('tasks', broker="redis://localhost:6379")

app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='Europe/Moscow',
)

app.conf.beat_schedule = {
    'add-every-5-seconds': {
        'task': 'e_logs.common.all_journals_app.tasks.hello',
        'schedule': 5.0,
    },
}

@app.task
def hello():
    print('Hello there!')