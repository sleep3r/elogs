from celery import Celery
from celery.schedules import crontab

from django.utils import timezone

from e_logs.common.all_journals_app.models import Shift, Cell
from e_logs.common.messages_app.models import Message

app = Celery('tasks', broker="redis://localhost:6379")

app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='Europe/Moscow',
)

app.conf.beat_schedule = {
    'run-while-furnace-shift-close': {
        'task': 'e_logs.common.all_journals_app.tasks.check_blank_shift',
        'schedule': crontab(hour='7,19', minute=59),
        'args': ("furnace",)
    },
    'run-while-leaching-shift-close': {
        'task': 'e_logs.common.all_journals_app.tasks.check_blank_shift',
        'schedule': crontab(hour='7,15,23', minute=59),
        'args': ("leaching",)
    },
    'run-while-electrolysis-shift-close': {
        'task': 'e_logs.common.all_journals_app.tasks.check_blank_shift',
        'schedule': crontab(hour='1,7,13,19', minute=59),
        'args': ("electrolysis",)
    },
}

@app.task
def check_blank_shift(plant):
    for shift in filter(lambda s:s.is_active,
            list(Shift.objects.filter(date=timezone.now(), journal__plant__name=plant))):
            if not Cell.objects.filter(group=shift).exists():
                shift.closed = True
                shift.save()

                Message.add(cell=None,
                            message={'type': 'blank_journal',
                                     'text': "Журнал остался незаполнен",
                                     'sendee':None },
                            plant=plant, positions=("Boss",))

                Message.add(cell=None,
                            message={'type': 'blank_journal',
                                     'text': "Журнал остался незаполнен",
                                     'sendee':None },
                            positions=("Big boss",))