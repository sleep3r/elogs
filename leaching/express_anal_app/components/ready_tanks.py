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

    items = tables.get_ready_product_table(shift)
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

    fields = [f.name for f in ReadyProduct._meta.get_fields(include_parents=False) if
              f.name != 'journaltable_ptr']
    tanks = ['3', '4', '5']

    print(request.POST)

    data = json.loads(request.POST['items'])
    date_time = datetime.datetime.now()

    for tank in tanks:
        id = data[tank]['id']
        currentTime = date_time.replace(hour=int(tank), minute=0, second=0, microsecond=0)
        print(id)
        model = ReadyProduct(pk=id)
        model.journal = journal
        model.shift = shift
        model.time = currentTime
        for field in fields:
            setattr(model, field, data[tank].get(field))
        model.save()
        print('Yoyoy!')
        msg = Message(type='critical_value', position='master laborant',
                text=f'Критические значения в полях: {model.get_critical()}')
        print('hello')
        msg.save()

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

    fields = [f.name for f in ReadyProduct._meta.get_fields(include_parents=False) if
              f.name != 'journaltable_ptr']
    tanks = ['3', '4', '5']

    print(request.POST)

    data = json.loads(request.POST['items'])
    date_time = datetime.datetime.now()

    for tank in tanks:
        currentTime = date_time.replace(hour=int(tank), minute=0, second=0, microsecond=0)
        model = ReadyProduct()
        model.journal = journal
        model.shift = shift
        model.time = currentTime
        for field in fields:
            setattr(model, field, data[tank].get(field))
        model.save()
        Message(type='critical_value', position='master laborant',
                text=f'Критические значения в полях: {model.get_critical()}').save()

    return {
        'result': 'ok'
    }
