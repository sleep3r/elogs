import json

from leaching.express_anal_app.services.messages import report_critical
from login_app.models import Message
from utils.webutils import parse, process_json_view
from leaching.express_anal_app import tables
from leaching.express_anal_app.journal_forms import *
from django.http import HttpResponseRedirect
from leaching.express_anal_app.models import *


@process_json_view(auth_required=False)
def get_table(request):

    if 'shift_id' in request.GET:
        shift = Shift.objects.get(id=request.GET['shift_id'])
    else:
        shift = Shift.objects.all()[0]

    items = tables.get_sample2_table(shift)
    return {
        'result': 'ok',
        'items': items,
        'current_count': len(items)
    }

@process_json_view(auth_required=False)
def save_record(request):
    data = json.loads(request.POST['items'])

    fields = ['cu', 'cd']
    date_time = datetime.datetime.now()

    for (num, item) in data.items():
        print(item)
        currentTime = date_time.replace(hour=int(item['time']), minute=0, second=0, microsecond=0)
        model = Sample2.objects.get(id=int(item['id']))
        for field in fields:
            if field in item:
                setattr(model, field, item.get(field) or 0)
        model.time = currentTime
        model.save()
        report_critical(model)

    return {
        'result': 'ok'
    }


@process_json_view(auth_required=False)
def add_record(request):
    journal = Journal.objects.get(name='Журнал экспресс анализов')

    if 'shift_id' in request.POST:
        shift = Shift.objects.get(id=request.POST['shift_id'])
    else:
        shift = Shift.objects.all()[0]

    print(shift.id)

    data = json.loads(request.POST['items'])
    print(data)
    date_time = datetime.datetime.now()
    fields = ['cu', 'cd']

    for (num, item) in data.items():
        print(item)
        currentTime = date_time.replace(hour=int(item['time']), minute=0, second=0, microsecond=0)
        model = Sample2()
        for field in fields:
            if field in item:
                setattr(model, field, item.get(field) or 0)
        model.journal = journal
        model.shift = shift
        model.time = currentTime
        model.save()
        report_critical(model)

    return {
        'result': 'ok'
    }
