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

    items = tables.get_shift_info_table(shift)
    return {
        'result': 'ok',
        'items': items,
        'current_count': len(items)
    }


@process_json_view(auth_required=False)
def save_record(request):
    data = json.loads(request.POST['items'])
    print(data)

    fields = [f.name for f in ShiftInfo._meta.get_fields(include_parents=False) if f.name not in ['journaltable_ptr',
                                                                                                  'employee',
                                                                                                  'this_master',
                                                                                                  'next_master']]
    record_id = data['id']
    model = ShiftInfo.objects.get(pk=record_id)
    for field in fields:
        if field in data:
            setattr(model, field, data[field])
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

    this_master = Employee.objects.get(pk=data['this_master'])
    next_master = Employee.objects.get(pk=data['next_master'])

    print(data['this_master'])

    fields = [f.name for f in ShiftInfo._meta.get_fields(include_parents=False) if f.name not in ['journaltable_ptr',
                                                                                                  'employee',
                                                                                                  'this_master',
                                                                                                  'next_master']]

    model = ShiftInfo()
    for field in fields:
        if field in data:
            setattr(model, field, data[field])
    model.this_master = this_master
    model.next_master = next_master
    model.journal = journal
    model.shift = shift
    model.time = date_time
    model.save()
    report_critical(model)

    return {
        'result': 'ok'
    }
