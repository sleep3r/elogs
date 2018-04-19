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

    items = tables.get_schieht_table(shift)
    return {
        'result': 'ok',
        'items': items,
        'current_count': len(items)
    }

@process_json_view(auth_required=False)
def save_record(request):
    data = json.loads(request.POST['items'])
    fields = [f.name for f in Schieht._meta.get_fields(include_parents=False) if f.name not in ['journaltable_ptr']]

    for num, item in data.items():
        print(item['id'])
        record_id = item['id']
        model = Schieht.objects.get(pk=record_id)
        for field in fields:
            if field in item:
                setattr(model, field, item[field])
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

    date_time = datetime.datetime.now()
    data = json.loads(request.POST['items'])
    fields = [f.name for f in Schieht._meta.get_fields(include_parents=False) if f.name not in ['journaltable_ptr','num']]

    for num, item in data.items():
        model = Schieht()
        for field in fields:
            if field in item:
                setattr(model, field, item[field])
        model.journal = journal
        model.shift = shift
        model.time = date_time
        model.num = num
        model.save()
        report_critical(model)

    return {
        'result': 'ok'
    }
