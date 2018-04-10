import json
from utils.webutils import parse, process_json_view
from leaching.express_anal_app import tables
from leaching.express_anal_app.journal_forms import *
from django.http import HttpResponseRedirect
from leaching.express_anal_app.models import *

def leaching_save_agitators(request):
    print('\n----FORM-----')
    print(request.POST['comment'])
    print('\n\n')
    journal = Journal.objects.all()[0]
    if 'shift_id' in request.POST:
        shift = Shift.objects.filter(id=request.POST['shift_id'])[0]
    else:
        shift = Shift.objects.all()[0]
    employee = Employee.objects.all()[0]
    agitators = ['13', '15', '17', '19']
    states = ['before', 'after']
    rows = ['1', '2', '3']

    fields = [
        'ph',
        'cu',
        'co',
        'cd',
        'h2so4'
    ]
    for num in agitators:
        for state in states:
            for rowNum in rows:
                model = {
                    'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
                    'journal': journal.id,
                    'shift': shift.id,
                    'employee': employee.id,
                    'num': num
                }
                model['before']   = 1 if state == 'before' else 0
                model['comment'] = request.POST['comment']
                for field in fields:
                    index = 'agitator' + num + '.'+ state + '.' + field + '_' + rowNum
                    print(index)
                    if index in request.POST:

                        model[field] = request.POST[index]

                form = AgitatorsForm(model)
                if form.is_valid():
                    form.save()
                else:
                    print(form.errors)

    return HttpResponseRedirect('leaching/all/edit')

@process_json_view(auth_required=False)
def leaching_api_agitators(request):

    if 'shift_id' in request.GET:
        shift = Shift.objects.get(id=request.GET['shift_id'])
    else:
        shift = Shift.objects.all()[0]

    return {
        'result': 'ok',
        'items': tables.get_agitators_table(shift)
    }


@process_json_view(auth_required=False)
def save_record(request):
    journal = Journal.objects.get(name='Журнал экспресс анализов')

    if 'shift_id' in request.POST:
        shift = Shift.objects.get(id=request.POST['shift_id'])
    else:
        shift = Shift.objects.all()[0]

    employee = Employee.objects.all()[0]

    data = json.loads(request.POST['items'])

    print(data['comment'])

    agitators = ['13', '15', '17', '19']
    before_state = ['true', 'false']
    fields = [f.name for f in Agitators._meta.get_fields(include_parents=False) if f.name != 'journaltable_ptr' and f.name != 'employee']

    dt = datetime.datetime.now()
    for key, item in data['times'].items():
        currentTime = dt.replace(hour=int(key)+1, minute=0, second=0, microsecond=0)
        for agit in agitators:
            for state in before_state:
                if 'id' in item[agit][state]:
                    id = item[agit][state]['id']
                    model = Agitators(pk=id)
                    model.shift = shift
                    model.journal = journal
                    model.num = agit
                    model.employee = employee
                    model.before = item[agit][state] == 'true'
                    model.time = currentTime
                else:
                    model = Agitators()
                    model.shift = shift
                    model.journal = journal
                    model.num = agit
                    model.employee = employee
                    model.time = currentTime
                    model.before = state == 'true'

                for field in fields:
                    setattr(model, field, item[agit][state].get(field))
                model.comment = data['comment']
                model.save()


    print(request.POST['shift_id'])

    return {
        'result': 'ok',
        'items': tables.get_agitators_table(shift)
    }
    return {'result': 'ok'}


@process_json_view(auth_required=False)
def add_record(request):
    journal = Journal.objects.get(name='Журнал экспресс анализов')

    if 'shift_id' in request.POST:
        shift = Shift.objects.get(id=request.POST['shift_id'])
    else:
        shift = Shift.objects.all()[0]

    employee = Employee.objects.all()[0]

    data = json.loads(request.POST['items'])
    agitators = ['13', '15', '17', '19']
    before_state = ['true', 'false']
    fields = [f.name for f in Agitators._meta.get_fields(include_parents=False) if
              f.name != 'journaltable_ptr' and f.name != 'employee']

    dt = datetime.datetime.now()
    key = 0
    for item in data['times']:
        currentTime = dt.replace(hour=int(key) + 1, minute=0, second=0, microsecond=0)
        key = key + 1
        for agitator in agitators:
            for state in before_state:
                model = Agitators()
                for field in fields:
                    setattr(model, field, item[agitator][state].get(field))
                model.shift = shift
                model.journal = journal
                model.num = agitator
                model.employee = employee
                model.time = currentTime
                model.before = state == 'true'
                if 'comment' in request.POST:
                    model.comment = request.POST['comment']
                else:
                    model.comment = '...'
                model.save()

    return {
        'result': 'ok',
        'added': [],
        'data': data
    }


@process_json_view(auth_required=False)
def add_agitators(request):
    return {}