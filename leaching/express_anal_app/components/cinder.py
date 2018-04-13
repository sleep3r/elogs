import json

from login_app.models import Message
from utils.webutils import parse, process_json_view
from leaching.express_anal_app import tables
from leaching.express_anal_app.journal_forms import *
from django.http import HttpResponseRedirect
from leaching.express_anal_app.models import *


@process_json_view(auth_required=False)
def leaching_cinder(request):

    if 'shift_id' in request.GET:
        shift = Shift.objects.get(id=request.GET['shift_id'])
    else:
        shift = Shift.objects.all()[0]

    items = tables.get_cinder_table(shift)
    return {
        'result': 'ok',
        'items': items,
        'current_count': len(items)
    }

@process_json_view(auth_required=False)
def save_record(request):
    journal = Journal.objects.get(name='Журнал экспресс анализов')

    if 'shift_id' in request.POST:
        shift = Shift.objects.get(id=request.POST['shift_id'])
    else:
        shift = Shift.objects.all()[0]

    fields = [f.name for f in Cinder._meta.get_fields(include_parents=False) if
              f.name != 'journaltable_ptr']
    print(request.POST)
    data = json.loads(request.POST['items'])
    print('---------')
    columns = ['0', '1']

    date_time = datetime.datetime.now()
    for col_num in columns:
        currentTime = date_time.replace(hour=int(col_num) + 1, minute=0, second=0, microsecond=0)
        if col_num in data:
            print(data[col_num]['id'])
            model = Cinder(pk=data[col_num]['id'])
            for field in fields:
                setattr(model, field, data[col_num].get(field))
            model.journal = journal
            model.shift = shift
            model.time = currentTime
            # model.col_num = int(col_num)
            model.save()

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

    employee = Employee.objects.all()[0]
    data = json.loads(request.POST['items'])
    fields = [f.name for f in Cinder._meta.get_fields(include_parents=False) if
              f.name != 'journaltable_ptr']
    columns = ['0', '1']
    date_time = datetime.datetime.now()

    for col_num in columns:
        currentTime = date_time.replace(hour=int(col_num) + 1, minute=0, second=0, microsecond=0)
        if col_num in data:
            model = Cinder()
            for field in fields:
                setattr(model, field, data[col_num].get(field))
            model.journal = journal
            model.shift = shift
            model.time = currentTime
            model.col_num = int(col_num)

            model.save()

    return {
        'result': 'ok'
    }
