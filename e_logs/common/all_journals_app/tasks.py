import os
from datetime import timedelta

from config import settings_setup

from celery import Celery

from django.core.management import call_command
from django.utils import timezone

from e_logs.core.models import Setting
from e_logs.common.all_journals_app.models import Shift, Cell, Journal
from e_logs.common.messages_app.models import Message
from e_logs.core.utils.webutils import get_or_none, current_date

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

@app.task
def create_shifts():
    def date_range(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    now_date = current_date()
    for journal in Journal.objects.all():
        if journal.type == 'shift':
            number_of_shifts = Shift.get_number_of_shifts(journal)
            for shift_date in date_range(now_date, now_date + timedelta(days=3)):
                for shift_order in range(1, number_of_shifts + 1):
                    Shift.objects.get_or_create(journal=journal, order=shift_order, date=shift_date)

@app.task
def check_blank_shifts():
    for shift in filter(lambda s:s.is_active(),list(Shift.objects.filter(
            date__range=[current_date() - timedelta(days=1), current_date()]))):
            if not shift.is_active(time=timezone.now()+timedelta(minutes=1)):
                check_for_no_cells(shift)

def check_for_no_cells(shift):
    if not Cell.objects.filter(group=shift).exists():
        shift.closed = True
        shift.save()

        Message.add(cell=None,
                    message={'type': 'blank_journal',
                             'text': "Журнал остался незаполнен",
                             'sendee': None},
                    plant_name=shift.journal.plant.name,
                    positions=("boss",))

        Message.add(cell=None,
                    message={'type': 'blank_journal',
                             'text': "Журнал остался незаполнен",
                             'sendee': None},
                    positions=("senior technologist",))

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
def dump_db():
    output = open(f'dumps/{current_date()}.json','w')
    call_command('dumpdata', stdout=output)
    output.close()
