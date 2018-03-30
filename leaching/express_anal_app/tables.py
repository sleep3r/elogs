import random
from collections import defaultdict

from leaching.express_anal_app.demo_database import DatabaseFiller
from leaching.express_anal_app.models import *
from pprint import pprint
from dateutil.parser import parse
from itertools import product

# from express_anal_app.tests import test_form_creation
from login_app.models import Employee
from leaching.express_anal_app.models import Employee, Shift, DenserAnal
from utils.deep_dict import deep_dict
from django.utils.translation import gettext as _

def add_model_to_dict(model, res, attrs=None):
    if attrs is None:
        attrs = [f.name for f in model._meta.get_fields(include_parents=False)]

    for attr in attrs:
        val = getattr(model, attr)
        if val is not None:
            res[attr] = val


def get_densers_table(shift=None, hour=None):
    if shift is None:
        shift = Shift.objects.all()[0]

    res = deep_dict()
    if hour is None:
        data = DenserAnal.objects.filter(shift=shift).order_by('time')
    else:
        data = DenserAnal.objects.filter(shift=shift, time__hour=hour).order_by('time')

    for d in data:
        for attr in ['ph', 'cu', 'fe', 'liq_sol']:
            time_index = int(d.time.strftime("%H"))
            res[time_index][d.point][d.sink][attr] = getattr(d, attr)

    return res.clear_empty().get_dict()


def get_leaching_express_anal_table(shift=None, hour=None):
    if shift is None:
        shift = Shift.objects.all()[0]

    res = deep_dict()
    if hour is None:
        data = LeachingExpressAnal.objects.filter(shift=shift).order_by('time')
    else:
        data = LeachingExpressAnal.objects.filter(shift=shift, time__hour=hour).order_by('time')

    for d in data:
        for attr in ['co', 'sb', 'cu', 'cu_st1', 'cd', 'solid_st1', 'ph', 'fe', 'arsenic', 'solid', 'current', 'density']:
            val = getattr(d, attr)
            if val is not None:
                time_index = int(d.time.strftime("%H"))
                res[time_index][d.point][attr] = val

    if hour is None:
        data = ProductionError.objects.filter(shift=shift).order_by('time')
    else:
        data = ProductionError.objects.filter(shift=shift, time__hour = hour).order_by('time')

    for d in data:
        for attr in ['norm', 'fact', 'error', 'correction', 'verified']:
            val = getattr(d, attr)
            if val is not None:
                time_index = int(d.time.strftime("%H"))
                res[time_index]['prod_correction'][attr] = val

    return res.clear_empty().get_dict()


def get_solutions_table(shift=None):
    if shift is None:
        shift = Shift.objects.all()[0]

    res = deep_dict()

    data = ZnPulpAnal.objects.filter(shift=shift)
    for d in data:
        combi_index = str(d.id) + ';' + str(d.cu_pulp_anal.id) + ';' + str(d.fe_solution_anal.id)
        for attr in ['liq_sol', 'ph', 't0', 'id', 'cu_pulp_anal']:
            val = getattr(d, attr)
            if val is not None:
                res[combi_index]['zn_pulp'][attr] = val

    data = CuPulpAnal.objects.filter(shift=shift)
    for d in data:
        combi_index = str(d.zn_pulp_anal.id) + ';' + str(d.id) + ';' + str(d.fe_solution_anal.id)
        for attr in ['liq_sol', 'before', 'after', 'solid', 'id']:
            val = getattr(d, attr)
            if val is not None:
                res[combi_index]['cu_pulp'][attr] = val

    data = FeSolutionAnal.objects.filter(shift=shift)
    for d in data:
        combi_index = str(d.zn_pulp_anal.id) + ';' + str(d.cu_pulp_anal.id) + ';' + str(d.id)
        for attr in ['h2so4', 'solid', 'sb', 'cu', 'fe', 'density', 'arsenic', 'cl', 'id']:
            val = getattr(d, attr)
            if val is not None:
                res[combi_index]['fe_sol'][attr] = val

    for i, k in enumerate(sorted(res.keys())):
        res[k]['num'] = i

    return res.clear_empty().get_dict()


def get_solutions2_table(shift=None):
    if shift is None:
        shift = Shift.objects.all()[0]
    items = DailyAnalysis.objects.filter(shift=shift)
    if len(items) == 0:
        return {}

    data = items[0]

    res = {}
    for attr in ['id', 'shlippe_sb', 'activ_sas', 'circulation_denser', 'fe_hi1', 'fe_hi2']:
        val = getattr(data, attr)
        if val is not None:
            res[attr] = val
    return res


def get_hydrometal1_table(shift=None):
    if shift is None:
        shift = Shift.objects.all()[0]

    res = deep_dict()
    for d in HydroMetal.objects.filter(shift=shift):
        time_index = d.time.strftime("%H:%M.%S")
        add_model_to_dict(d, res[time_index][str(d.mann_num)])
        res[time_index][str(d.mann_num)]['id'] = d.id

    return res.clear_empty().get_dict()


def get_cinder_gran_table(shift=None):
    if shift is None:
        shift = Shift.objects.all()[0]

    res = deep_dict()
    data = CinderDensity.objects.filter(shift=shift)
    data = data[0] if data else CinderDensity()
    for attr in ['gran_avg', 'fe_avg', 'fe_shave']:
        val = getattr(data, attr)
        if val is not None:
            res[attr] = val

    res['id'] = data.id
    for d in CinderDensity.objects.filter(shift=shift):
        add_model_to_dict(d, res['grans'][str(d.time)], attrs=['gran'])

    return res.clear_empty().get_dict()


def get_agitators_table(shift=None):
    if shift is None:
        shift = Shift.objects.all()[0]

    res = deep_dict()
    for d in Agitators.objects.filter(shift=shift):
        add_model_to_dict(d, res['times'][d.time][d.num][d.before])

    agts = Agitators.objects.filter(shift=shift)
    res['comment'] = agts[0].comment if agts else ''

    times = deep_dict()
    for i, k in enumerate(sorted(res['times'].keys())):
        times[i] = res['times'][k]

    res['times'] = times

    return res.clear_empty().get_dict()


# sheet 2
def get_neutral_densers_table(shift=None):
    if shift is None:
        shift = Shift.objects.all()[0]

    res = deep_dict()
    for d in NeutralDenser.objects.filter(shift=shift):
        add_model_to_dict(d, res[str(d.num)])

    return res.clear_empty().get_dict()


def get_ready_product_table(shift=None):
    if shift is None:
        shift = Shift.objects.all()[0]

    res = deep_dict()
    for d in ReadyProduct.objects.filter(shift=shift):
        add_model_to_dict(d, res[str(d.num)])

    return res.clear_empty().get_dict()


def get_free_tanks_table(shift=None):
    if shift is None:
        shift = Shift.objects.all()[0]

    res = deep_dict()
    for d in FreeTank.objects.filter(shift=shift):
        add_model_to_dict(d, res[str(d.str_num)])

    return res.clear_empty().get_dict()


def get_neutral_solution_table(shift=None):
    if shift is None:
        shift = Shift.objects.all()[0]

    res = deep_dict()
    for d in NeutralSolution.objects.filter(shift=shift):
        add_model_to_dict(d, res[str(d.str_num)])

    return res.clear_empty().get_dict()


def get_shift_info_table(shift=None):
    if shift is None:
        shift = Shift.objects.all()[0]

    res = deep_dict()
    items = ShiftInfo.objects.filter(shift=shift)
    if len(items) == 0:
        return {}
    d = items[0]
    add_model_to_dict(d, res)

    res['date'] = shift.date
    res['master'] = shift.master
    res['laborant'] = shift.laborant
    res['shift_num'] = shift.order

    return res.clear_empty().get_dict()


def get_self_security_table(shift=None):
    if shift is None:
        shift = Shift.objects.all()[0]

    res = deep_dict()
    data = SelfSecurity.objects.filter(shift=shift).order_by('time')[:3]
    res['bignote'] = data[0].bignote if data else ''

    for i, d in enumerate(data):
        res['notes'][i]['time'] = d.time
        res['notes'][i]['note'] = d.note

    return res.clear_empty().get_dict()


def get_schieht_table(shift=None):
    if shift is None:
        shift = Shift.objects.all()[0]

    res = deep_dict()
    data = Schieht.objects.filter(shift=shift)

    for d in data:
        add_model_to_dict(d, res[str(d.num)])

    return res.clear_empty().get_dict()


def get_cinder_table(shift=None):
    if shift is None:
        shift = Shift.objects.all()[0]

    res = deep_dict()
    data = Cinder.objects.filter(shift=shift)

    for d in data:
        add_model_to_dict(d, res[str(d.col_num)])

    return res.clear_empty().get_dict()


def get_electrolysis_table(shift=None):
    if shift is None:
        shift = Shift.objects.all()[0]

    res = deep_dict()
    data = Electrolysis.objects.filter(shift=shift)

    for d in data:
        add_model_to_dict(d, res['series'][d.series])
    res['comment'] = data[0].comment if data else ''

    return res.clear_empty().get_dict()


def get_reagents_table(shift=None):
    if shift is None:
        shift = Shift.objects.all()[0]

    res = deep_dict()
    data = Reagents.objects.filter(shift=shift)

    for d in data:
        if d.state != 'none':
            add_model_to_dict(d, res['states'][d.state])
        else:
            res['stages_zn_dust'][d.stage] = d.zn_dust

    res['fence_state'] = data[0].fence_state if data else ''

    return res.clear_empty().get_dict()


# this method can be called by typing "python manage.py my_command"
def command_to_process():
    df = DatabaseFiller()
    df.recreate_database()

    # df.clean_database()
    a = get_densers_table()
    pprint(a)