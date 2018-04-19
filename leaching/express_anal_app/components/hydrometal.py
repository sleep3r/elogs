import json

from leaching.express_anal_app.services.messages import report_critical
from login_app.models import Message
from utils.webutils import parse, process_json_view
from leaching.express_anal_app import tables
from leaching.express_anal_app.journal_forms import *
from django.http import HttpResponseRedirect
from leaching.express_anal_app.models import *


@process_json_view(auth_required=False)
def leaching_api_hydrometal(request):
    if 'shift_id' in request.GET:
        shift = Shift.objects.filter(id=request.GET['shift_id'])[0]
    else:
        shift = Shift.objects.all()[0]

    items = tables.get_hydrometal1_table(shift)

    return {
        'result': 'ok',
        'items': items,
        'count': len(items),
        'extra': tables.get_cinder_gran_table(shift)
    }

@process_json_view(auth_required=False)
def leaching_save_hydrometal_json(request):
    journal = Journal.objects.all()[0]
    if 'shift_id' in request.POST:
        shift = Shift.objects.filter(id=request.POST['shift_id'])[0]
    else:
        shift = Shift.objects.all()[0]
    employee = Employee.objects.all()[0]
    manns = ['1', '4']
    fields = [
        'ph',
        'acid',
        'fe2',
        'fe_total',
        'cu',
        'sb',
        'sediment',
    ]

    for mannNum in manns:
        model = {
            'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
            'journal': journal.id,
            'shift': shift.id,
            'employee': employee.id
        }
        model['mann_num'] = mannNum
        for field in fields:
            index = 'mann' + mannNum + '.' + field
            if index in request.POST:
                model[field] = request.POST[index]

        form = HydrometalForm(model)
        if form.is_valid():
            form.save()
            report_critical(model)
        else:
            print(form.errors)

    return {
        'result': 'ok',
        'items': tables.get_hydrometal1_table(shift),
        'extra': tables.get_cinder_gran_table(shift)
    }


@process_json_view(auth_required=False)
def leaching_update_hydrometal(request):
    journal = Journal.objects.all()[0]
    data = json.loads(request.POST['item'])

    print(data['shift_id'])
    print(data['extra'])

    if 'shift_id' in data:
        shift = Shift.objects.get(id=data['shift_id'])
    else:
        shift = Shift.objects.all()[0]
    employee = Employee.objects.all()[0]

    fields = [
        'ph',
        'acid',
        'fe2',
        'fe_total',
        'cu',
        'sb',
        'sediment',
        'mann_num'
    ]

    extra_id = data['extra']['id']
    extra_fields = [
        'gran',
        'gran_avg',
        'fe_avg',
        'fe_shave'
    ]

    if extra_id is None:
        cinder_model = CinderDensity()
    else:
        cinder_model = CinderDensity.objects.get(pk=extra_id)

    setattr(cinder_model, 'journal', journal)
    setattr(cinder_model, 'shift', shift)
    for field in extra_fields:
        if field in data['extra']:
            setattr(cinder_model, field, data['extra'][field])

    cinder_model.save()
    report_critical(cinder_model)

    manns = ['1','4']
    for man in manns:
        item = data[man]
        if 'id' in item:
            model = HydroMetal.objects.get(pk=item['id'])
        else:
            model = HydroMetal()
            setattr(model, 'mann_num', man)
            setattr(model, 'journal', journal)
            setattr(model, 'shift', shift)
            setattr(model, 'employee', employee)

        for field in fields:
            if field in item:
                setattr(model, field, item[field])
        model.save()
        report_critical(model, where=man)


    return {
        'result': 'ok',
    }


@process_json_view(auth_required=False)
def leaching_save_hydrometal_remove(request):
    ids = filter(None, request.GET['ids'].split(':'))

    for record_id in ids:
        record = HydroMetal.objects.filter(id=record_id).delete()

    return {
        'action': 'remove',
        'id': ids,
        'record': record
    }
