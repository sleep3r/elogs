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

    items = tables.get_free_tanks_table(shift)
    return {
        'result': 'ok',
        'items': items,
        'current_count': len(items)
    }

@process_json_view(auth_required=False)
def save_record(request):
    fields = ['prev_measure', 'cur_measure', 'deviation']
    data = json.loads(request.POST['items'])

    for (key, item) in data.items():
        print(item)
        # print(key)
        id = item['id']
        model = FreeTank.objects.get(pk=id)
        for field in fields:
            if field in item:
                setattr(model, field, item[field])
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

    fields = ['prev_measure', 'cur_measure', 'deviation', 'tank_name']
    data = json.loads(request.POST['items'])
    date_time = datetime.datetime.now()

    for (key, item) in data.items():
        print(item)
        model = FreeTank()
        for field in fields:
            if field in item:
                setattr(model, field, item[field])
        model.str_num = key
        model.journal = journal
        model.shift = shift
        model.time = date_time.replace(hour=int(key) + 1, minute=0, second=0, microsecond=0)
        model.save()

    return {
        'result': 'ok'
    }
