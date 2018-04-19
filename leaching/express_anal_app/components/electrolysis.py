import json

from login_app.models import Message
from utils.webutils import parse, process_json_view
from leaching.express_anal_app import tables
from leaching.express_anal_app.journal_forms import *
from django.http import HttpResponseRedirect
from leaching.express_anal_app.models import *
import decimal


@process_json_view(auth_required=False)
def get_table(request):

    if 'shift_id' in request.GET:
        shift = Shift.objects.get(id=request.GET['shift_id'])
    else:
        shift = Shift.objects.all()[0]

    items = tables.get_electrolysis_table(shift)
    return {
        'result': 'ok',
        'items': items,
        'current_count': len(items)
    }


@process_json_view(auth_required=False)
def save_record(request):
    data = json.loads(request.POST['items'])
    fields = [f.name for f in Electrolysis._meta.get_fields(include_parents=False) if f.name not in ['journaltable_ptr']]
    for num, item in data['series'].items():
        print(item)
        record_id = item['id']
        model = Electrolysis.objects.get(pk=record_id)
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

    date_time = datetime.datetime.now()

    data = json.loads(request.POST['items'])
    print(data['series'])
    fields = [f.name for f in Electrolysis._meta.get_fields(include_parents=False) if f.name not in ['journaltable_ptr',
                                                                                                     'series',
                                                                                                     'comment']]
    # TODO: fix this
    for num, item in data['series'].items():
        seriea = int(num)
        model = Electrolysis()
        for field in fields:
            if field in item:
                setattr(model, field, item.get(field) or 0.0)


        model.series = seriea
        model.journal = journal
        model.shift = shift
        model.time = date_time
        model.comment = 'comm'
        model.save()

    return {
        'result': 'ok'
    }
