import json
from django.http import HttpResponseRedirect
from leaching.express_anal_app.models import *
from utils.webutils import parse, process_json_view
from leaching.express_anal_app import tables


@process_json_view(auth_required=False)
def add_record(request):
    record = json.loads(request.POST['record'])
    shift_id = request.POST['shift_id']
    hour = int(request.POST['hour'])

    journal = Journal.objects.get(name='Журнал экспресс анализов')
    if shift_id is not None:
        shift = Shift.objects.get(id=shift_id)
        if shift is None:
            shift = Shift.objects.all()[0]
    else:
        shift = Shift.objects.all()[0]

    densers = ['10', '11', '12']
    sinks = ['hs', 'ls']
    fields = [
        'ph',
        'cu',
        'fe',
        'liq_sol',
    ]
    dt = datetime.datetime.now()

    for denser in densers:
        for sink in sinks:
            model = DenserAnal()
            model.point = denser
            model.sink = sink
            model.journal = journal
            model.shift = shift
            for field in fields:
                setattr(model, field, record[denser][sink].get(field))
            model.time = dt.replace(hour=hour, minute=0, second=0, microsecond=0)
            model.save()

    return {
        'result': 'ok'
    }


@process_json_view(auth_required=False)
def save_record(request):
    data = json.loads(request.POST['record'])
    record = data["item"]
    shift_id = request.POST['shift_id']
    hour = int(request.POST['hour'])
    journal = Journal.objects.get(name='Журнал экспресс анализов')
    if shift_id is not None:
        shift = Shift.objects.get(id=shift_id)
        if shift is None:
            shift = Shift.objects.all()[0]
    else:
        shift = Shift.objects.all()[0]

    densers = ['10', '11', '12']
    sinks = ['hs', 'ls']
    fields = [
        'ph',
        'cu',
        'fe',
        'liq_sol',
    ]
    dt = datetime.datetime.now()

    for (num, denser) in record.items():
        for sink in sinks:
            if 'id' in denser[sink]:
                record_id = denser[sink]['id']
                model = DenserAnal.objects.get(id=record_id)
                model.point = str(num)
                model.sink = sink
                model.journal = journal
                model.shift = shift
                for field in fields:
                    setattr(model, field, denser[sink].get(field))
                model.time = dt.replace(hour=hour, minute=0, second=0, microsecond=0)
                model.save()

    return {
        'result': 'ok'
    }


@process_json_view(auth_required=False)
def get_table(request):
    if 'shift_id' in request.GET:
        shift = Shift.objects.get(id=request.GET['shift_id']) or None
    else:
        shift = Shift.objects.all()[0]

    if 'hour' in request.GET:
        hour = request.GET['hour']
        items = tables.get_densers_table(shift, hour)
    else:
        items = tables.get_densers_table(shift)
    return {
        'result': 'ok',
        'items': items,
        'count': len(items)
    }


@process_json_view(auth_required=False)
def leaching_save_densers_json(request):
    journal = Journal.objects.all()[0]

    if 'shift_id' in request.POST:
        shift = Shift.objects.filter(id=request.POST['shift_id'])[0]
    else:
        shift = Shift.objects.all()[0]

    densers = ['10', '11', '12']
    sinks = ['hs', 'ls']
    fields = [
        'ph',
        'cu',
        'fe',
        'liq_sol',
    ]

    form_errors = ''

    for denser in densers:
        for sink in sinks:
            model = {
                'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
                'journal': journal.id,
                'shift': shift.id
            }

            model['point'] = denser
            model['sink'] = sink
            hour = int(request.POST['select_time'])
            dt = datetime.datetime.now()
            model['time'] = dt.replace(hour=hour, minute=0, second=0, microsecond=0)

            for field in fields:
                postIndex = 'denser_' + denser + '.' + sink + '.' + field
                if postIndex in request.POST:
                    model[field] = request.POST[postIndex]

            form = jea_stand_forms['DenserAnal'](model)
            if form.is_valid():
                form.save()
            else:
                form_errors = form.errors
                print(form.errors)

    return {
        'result': 'ok',
        'items': tables.get_densers_table(shift),
        'post': dict(request.POST),
        'form_errors': form_errors
    }
