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

    items = tables.get_reagents_table(shift)
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

    states = [
        'delivered',
        'taken',
        'consumption',
        'issued',
    ]

    stages = [
        '1st',
        '2st',
        '3st',
        'cd',
        'total'
    ]

    employee = Employee.objects.all()[0]
    data = json.loads(request.POST['items'])
    fields = [f.name for f in Reagents._meta.get_fields(include_parents=False) if
              f.name != 'journaltable_ptr' if f.name != 'stage' if f.name != 'state']

    date_time = datetime.datetime.now()

    currentTime = date_time.replace(hour=int(8), minute=0, second=0, microsecond=0)

    for state in states:
        model = Reagents()
        if state in data['states']:
            for field in fields:
                setattr(model, field, data['states'][state].get(field))

        model.journal = journal
        model.shift = shift
        model.time = currentTime
        model.fence_state = data['fence_state']
        model.state = state
        model.stage = 'total'
        model.save()

    for stage in stages:
        model = Reagents()
        model.journal = journal
        model.shift = shift
        model.time = currentTime
        model.fence_state = data['fence_state']
        model.stage = stage
        model.state = 'none'
        if stage in data['stages_zn_dust']:
            model.zn_dust = data['stages_zn_dust'][stage]
            print(model.zn_dust)
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

    states = [
        'delivered',
        'taken',
        'consumption',
        'issued',
    ]

    stages = [
        '1st',
        '2st',
        '3st',
        'cd',
        'total'
    ]

    employee = Employee.objects.all()[0]
    data = json.loads(request.POST['items'])
    fields = [f.name for f in Reagents._meta.get_fields(include_parents=False) if
              f.name != 'journaltable_ptr' if f.name != 'stage' if f.name != 'state' ]

    date_time = datetime.datetime.now()

    currentTime = date_time.replace(hour=int(8), minute=0, second=0, microsecond=0)

    for state in states:
        model = Reagents()
        if state in data['states']:
            for field in fields:
                setattr(model, field, data['states'][state].get(field))

        model.journal = journal
        model.shift = shift
        model.time = currentTime
        model.fence_state = data['fence_state']
        model.state = state
        model.stage = 'total'
        model.save()

    for stage in stages:
        model = Reagents()
        model.journal = journal
        model.shift = shift
        model.time = currentTime
        model.fence_state = data['fence_state']
        model.stage = stage
        model.state = 'none'
        if stage in data['stages_zn_dust']:
            model.zn_dust = data['stages_zn_dust'][stage]
            print(model.zn_dust)
        model.save()


    return {
        'result': 'ok'
    }
