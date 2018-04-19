import json

from leaching.express_anal_app.services.messages import report_critical
from login_app.models import Message
from utils.webutils import parse, process_json_view
from leaching.express_anal_app import tables
from leaching.express_anal_app.journal_forms import *
from django.http import HttpResponseRedirect
from leaching.express_anal_app.models import *
from django.contrib.auth.decorators import login_required


@process_json_view(auth_required=False)
def remove_record(request):
    combid = request.GET['combid']
    ids = combid.split('-')

    record_id = ids[0]
    if record_id is not None:
        record = ZnPulpAnal.objects.filter(id=record_id).delete()

    return {
        'action': 'remove',
        'id': id,
        'record': record
    }


@login_required
def leaching_save_pulps(request):

    journal = Journal.objects.all()[0]
    if 'shift_id' in request.POST:
        shift = Shift.objects.filter(id=request.POST['shift_id'])[0]
    else:
        shift = Shift.objects.all()[0]
    formsCodes = ['zn_pulp', 'cu_pulp', 'fe_sol']
    fields = [
        'liq_sol',
        'ph',
        't0',
        'before',
        'after',
        'solid',
        'h2so4',
        'sb',
        'cu',
        'fe',
        'density',
        'arsenic',
        'cl',
    ]

    for formCode in formsCodes:
        model = {
            'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
            'journal': journal.id,
            'shift': shift.id
        }
        for field in fields:
            postIndex = formCode + '.' + field
            if postIndex in request.POST:
                model[field] = request.POST[postIndex]

        if formCode == 'zn_pulp':
            form = ZnPulpForm(model)
        elif formCode == 'cu_pulp':
            form = CuPulpForm(model)
        elif formCode == 'fe_sol':
            form = FeSolutionForm(model)

        if form.is_valid():
            form.save()
            report_critical(model)
        else:
            print(form.errors)

    return HttpResponseRedirect('leaching/all/edit')


@process_json_view(auth_required=False)
def get_table(request):
    if 'shift_id' in request.GET:
        shift = Shift.objects.get(id=request.GET['shift_id'])
    else:
        shift = Shift.objects.all()[0]

    return {
        'result': 'ok',
        'items': tables.get_solutions_table(shift),
        'extra': tables.get_solutions2_table(shift)
    }


@process_json_view(auth_required=False)
def leaching_update_pulps(request):
    journal = Journal.objects.get(name='Журнал экспресс анализов')
    data = json.loads(request.POST['item'])

    print(data['extra'])
    if 'shift_id' in data:
        shift = Shift.objects.get(id=data['shift_id'])
    else:
        shift = Shift.objects.all()[0]

    zn_fields = [f.name for f in ZnPulpAnal._meta.get_fields(include_parents=False) if f.name != 'cu_pulp_anal' if f.name != 'fe_solution_anal' if f.name != 'journaltable_ptr']
    cu_fields = [f.name for f in CuPulpAnal._meta.get_fields(include_parents=False) if f.name != 'zn_pulp_anal' if f.name != 'fe_solution_anal' if f.name != 'journaltable_ptr']
    fe_fields = [f.name for f in FeSolutionAnal._meta.get_fields(include_parents=False) if f.name != 'cu_pulp_anal' if f.name != 'zn_pulp_anal' if f.name != 'journaltable_ptr']
    da_fields = [f.name for f in DailyAnalysis._meta.get_fields(include_parents=False) if f.name != 'journaltable_ptr']

    if 'id' in data['zn_pulp']:
        zn_pulp = ZnPulpAnal.objects.get(pk=int(data['zn_pulp']['id']))
    else:
        zn_pulp = ZnPulpAnal()

    if 'id' in data['cu_pulp']:
        cu_pulp = CuPulpAnal.objects.get(pk=int(data['cu_pulp']['id']))
    else:
        cu_pulp = CuPulpAnal()

    if 'id' in data['fe_sol']:
        fe_sol = FeSolutionAnal.objects.get(pk=int(data['fe_sol']['id']))
    else:
        fe_sol = FeSolutionAnal()

    if 'id' in data['extra']:
        day_anal = DailyAnalysis.objects.get(pk=int(data['extra']['id']))
    else:
        day_anal = DailyAnalysis()

    for field in da_fields:
        if field in data['extra']:
            setattr(day_anal, field, data['extra'].get(field))
        else:
            setattr(day_anal, field, '')
    day_anal.journal = journal
    day_anal.shift = shift
    day_anal.save()
    report_critical(day_anal)

    for field in zn_fields:
        setattr(zn_pulp, field, data['zn_pulp'].get(field) or 0)

    setattr(zn_pulp,'shift', shift)
    zn_pulp.journal = journal
    zn_pulp.cu_pulp_anal = cu_pulp
    zn_pulp.fe_sol_anal = fe_sol
    zn_pulp.save()
    report_critical(zn_pulp)

    for field in cu_fields:
        setattr(cu_pulp, field, data['cu_pulp'].get(field) or 0)
    setattr(cu_pulp, 'shift', shift)
    cu_pulp.zn_pulp_anal = zn_pulp
    cu_pulp.fe_sol_anal = fe_sol
    cu_pulp.journal = journal
    cu_pulp.save()
    report_critical(model)

    for field in fe_fields:
        setattr(fe_sol, field, data['fe_sol'].get(field) or 0)
    setattr(fe_sol, 'shift', shift)
    fe_sol.zn_pulp_anal = zn_pulp
    fe_sol.cu_pulp_anal = cu_pulp
    fe_sol.save()
    report_critical(fe_sol)

    return {
        'result': 'ok',
        'data': data,
    }

@process_json_view(auth_required=False)
def add_record(request):
    journal = Journal.objects.get(name='Журнал экспресс анализов')
    data = json.loads(request.POST['item'])

    print(request.POST)

    if 'shift_id' in data:
        shift = Shift.objects.get(id=data['shift_id'])
    else:
        shift = Shift.objects.all()[0]

    zn_fields = [f.name for f in ZnPulpAnal._meta.get_fields(include_parents=False) if f.name != 'cu_pulp_anal' if f.name != 'fe_solution_anal' if f.name != 'journaltable_ptr']
    cu_fields = [f.name for f in CuPulpAnal._meta.get_fields(include_parents=False) if f.name != 'zn_pulp_anal' if f.name != 'fe_solution_anal' if f.name != 'journaltable_ptr']
    fe_fields = [f.name for f in FeSolutionAnal._meta.get_fields(include_parents=False) if f.name != 'cu_pulp_anal' if f.name != 'zn_pulp_anal' if f.name != 'journaltable_ptr']
    da_fields = [f.name for f in DailyAnalysis._meta.get_fields(include_parents=False) if f.name != 'journaltable_ptr']

    if 'id' in data['zn_pulp']:
        zn_pulp = ZnPulpAnal.objects.get(pk=int(data['zn_pulp']['id']))
    else:
        zn_pulp = ZnPulpAnal()

    if 'id' in data['cu_pulp']:
        cu_pulp = CuPulpAnal.objects.get(pk=int(data['cu_pulp']['id']))
    else:
        cu_pulp = CuPulpAnal()

    if 'id' in data['fe_sol']:
        fe_sol = FeSolutionAnal.objects.get(pk=int(data['fe_sol']['id']))
    else:
        fe_sol = FeSolutionAnal()

    if 'id' in data['extra']:
        day_anal = DailyAnalysis.objects.get(pk=int(data['extra']['id']))
    else:
        day_anal = DailyAnalysis()

    for field in da_fields:
        if field in data['extra']:
            setattr(day_anal, field, data['extra'].get(field))
        else:
            setattr(day_anal, field, ' ')
    day_anal.journal = journal
    day_anal.shift = shift
    day_anal.save()

    for field in zn_fields:

        setattr(zn_pulp, field, data['zn_pulp'].get(field) or 0)

    setattr(zn_pulp, 'shift', shift)
    zn_pulp.journal = journal
    zn_pulp.cu_pulp_anal = cu_pulp
    zn_pulp.fe_sol_anal = fe_sol
    zn_pulp.save()

    for field in cu_fields:
        setattr(cu_pulp, field, data['cu_pulp'].get(field) or 0)
    setattr(cu_pulp, 'shift', shift)
    cu_pulp.zn_pulp_anal = zn_pulp
    cu_pulp.fe_sol_anal = fe_sol
    cu_pulp.journal = journal
    cu_pulp.save()

    for field in fe_fields:
        setattr(fe_sol, field, data['fe_sol'].get(field) or 0)
    setattr(fe_sol, 'shift', shift)
    fe_sol.zn_pulp_anal = zn_pulp
    fe_sol.cu_pulp_anal = cu_pulp
    fe_sol.save()

    return {
        'result': 'ok',
        'data': data
    }
