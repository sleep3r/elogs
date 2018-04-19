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

    data = json.loads(request.POST['items'])
    fence_comment = data['fence_state']
    fields = [f.name for f in Reagents._meta.get_fields(include_parents=False) if
              f.name != 'journaltable_ptr' if f.name != 'stage' if f.name != 'state']

    date_time = datetime.datetime.now()

    currentTime = date_time.replace(hour=int(8), minute=0, second=0, microsecond=0)

    for state in states:
        if state in data['states']:
            if 'id' in data['states'][state]:
                record_id = data['states'][state]['id']
                model = Reagents.objects.get(pk=record_id)
            else:
                model = Reagents()

            for field in fields:
                setattr(model, field, data['states'][state].get(field))

            model.journal = journal
            model.shift = shift
            model.time = currentTime
            model.fence_state = fence_comment
            model.state = state
            model.stage = 'total'
            model.save()
            report_critical(model)

    for stage in stages:
        if 'id' in data['stages_zn_dust']:
            record_id = data['stages_zn_dust']['id']
            model = Reagents.objects.get(pk=record_id)
        else:
            model = Reagents()

        if stage in data['stages_zn_dust']:
            model.zn_dust = data['stages_zn_dust'][stage]

        model.journal = journal
        model.shift = shift
        model.time = currentTime
        model.fence_state = fence_comment
        model.stage = stage
        model.state = 'none'
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

    data = json.loads(request.POST['items'])
    fence_comment = data['fence_state']
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
        model.fence_state = fence_comment
        model.state = state
        model.stage = 'total'
        model.save()
        report_critical(model)

    for stage in stages:
        model = Reagents()
        model.journal = journal
        model.shift = shift
        model.time = currentTime
        model.fence_state = fence_comment
        model.stage = stage
        model.state = 'none'
        if stage in data['stages_zn_dust']:
            model.zn_dust = data['stages_zn_dust'][stage]
        model.save()
        report_critical(model)


    return {
        'result': 'ok'
    }
