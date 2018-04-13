import json

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

    items = tables.get_neutral_solution_table(shift)
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

    data = json.loads(request.POST['items'])

    date_time = datetime.datetime.now()
    currentTime = date_time.replace(hour=int(8), minute=0, second=0, microsecond=0)
    for (key, item) in data.items():
        id = int(item['id'])
        print(id)
        model = NeutralSolution.objects.get(pk=id)
        model.journal = journal
        model.shift = shift
        model.value = item['value']
        model.save()
        Message(type='critical_value', position='master laborant',
                text=f'Критические значения в полях: {model.get_critical()}').save()

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

    data = json.loads(request.POST['items'])
    print(data)
    date_time = datetime.datetime.now()
    currentTime = date_time.replace(hour=int(8), minute=0, second=0, microsecond=0)
    for (key, item) in data.items():
        model = NeutralSolution()
        model.journal = journal
        model.shift = shift
        model.str_num = key
        if 'value' in item:
            model.value = item['value']
        else:
            model.value = 0
        model.time = currentTime
        model.save()
        Message(type='critical_value', position='master laborant',
                text=f'Критические значения в полях: {model.get_critical()}').save()

    return {
        'result': 'ok'
    }
