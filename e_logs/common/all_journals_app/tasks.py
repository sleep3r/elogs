import os
from datetime import timedelta

from config import settings_setup

from celery import Celery
from celery.schedules import crontab

from django.utils import timezone

from e_logs.business_logic.modes.models import Mode
from e_logs.core.models import Setting
from e_logs.common.all_journals_app.models import Shift, Cell, Journal
from e_logs.common.messages_app.models import Message
from e_logs.core.utils.webutils import get_or_none


if os.environ.get('DOCKER') == 'yes':
    app = Celery('tasks', broker="redis://redis:6379")
else:
    app = Celery('tasks', broker="redis://localhost:6379")

app.config_from_object('django.conf:settings', namespace='CELERY')

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
    'run-while-OC-shift-close': {
        'task': 'e_logs.common.all_journals_app.tasks.check_blank_OC_shift',
        'schedule': crontab(hour='7,15,23', minute=59),
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
    'create-shifts': {
        'task': 'e_logs.common.all_journals_app.tasks.create_shifts',
        'schedule': crontab(hour='0', minute=0),
    },
}


@app.task
def create_shifts():

    def date_range(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    now_date = timezone.now().date()
    for journal in Journal.objects.all():
        if journal.type == 'shift':
            number_of_shifts = Shift.get_number_of_shifts(journal)
            for shift_date in date_range(now_date, now_date + timedelta(days=3)):
                for shift_order in range(1, number_of_shifts + 1):
                    Shift.objects.get_or_create(journal=journal, order=shift_order, date=shift_date)

@app.task
def check_blank_shift(plant):
    for shift in filter(lambda s:s.is_active,
            list(Shift.objects.filter(journal__plant__name=plant).
                         exclude(journal__name="reports_furnace_area"))):
            if not Cell.objects.filter(group=shift).exists():
                shift.closed = True
                shift.save()

                Message.add(cell=None,
                            message={'type': 'blank_journal',
                                     'text': "Журнал остался незаполнен",
                                     'sendee': None },
                            plant=plant, positions=("Boss",))

                Message.add(cell=None,
                            message={'type': 'blank_journal',
                                     'text': "Журнал остался незаполнен",
                                     'sendee': None },
                            positions=("Big boss",))

@app.task
def end_of_limited_access(page_id):
    page = get_or_none(Shift, id=page_id)
    if page:
        Setting.of(page)['limited_access_employee_id_list'] = None

@app.task
def send_deferred_message(type, text, ids):
    Message.add(cell=None,
                message={'type': type,
                         'text': text,
                         'sendee': None},
                uids=ids)

@app.task
def end_of_mode(mode_id):
    mode = get_or_none(Mode, id=mode_id)
    if mode:
        mode.is_active = False
        mode.save()
