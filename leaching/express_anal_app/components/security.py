import json
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

    items = tables.get_self_security_table(shift)
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

    print(request.POST)
    employee = Employee.objects.all()[0]

    data = json.loads(request.POST['items'])
    hours = ['0', '1', '2']

    print(data)
    date_time = datetime.datetime.now()

    for hour in hours:
        id = data['notes'][hour]['id']
        model = SelfSecurity.objects.get(pk=id)
        currentTime = date_time.replace(hour=int(hour)+1, minute=0, second=0, microsecond=0)
        model.note = data['notes'][hour]['note']
        model.bignote = data['bignote']
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

    print(request.POST)
    employee = Employee.objects.all()[0]

    data = json.loads(request.POST['items'])
    hours = ['0', '1', '2']

    print(data)

    date_time = datetime.datetime.now()

    for hour in hours:
        model = SelfSecurity()
        currentTime = date_time.replace(hour=int(hour) + 1, minute=0, second=0, microsecond=0)
        model.note = data['notes'][hour]['note']
        model.bignote = data['bignote']
        model.journal = journal
        model.shift = shift
        model.time = currentTime

        model.save()

    return {
        'result': 'ok'
    }
