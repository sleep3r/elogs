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

    items = tables.get_veu_table(shift)
    return {
        'result': 'ok',
        'items': items,
        'current_count': len(items)
    }

@process_json_view(auth_required=False)
def save_record(request):
    data = json.loads(request.POST['items'])
    fields = [
            'num',
            'hot',
            'cold',
    ]

    numbers = ['1', '2', '3']

    for (rec_id, item) in data.items():
        print(item)
        model = VEU.objects.get(id=int(item['id']))
        for field in fields:
            if field in item:
                setattr(model, field, item.get(field) or 0)

        model.comment = ' '
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

    data = json.loads(request.POST['items'])
    date_time = datetime.datetime.now()
    fields = [
        'num',
        'hot',
        'cold',
        'comment'
    ]

    for (num, item) in data.items():
        model = VEU()
        for field in fields:
            if field in item:
                setattr(model, field, item.get(field) or 0)

        model.journal = journal
        model.shift = shift
        model.time = date_time
        model.comment = ' '
        model.save()

    return {
        'result': 'ok'
    }
