import random
from collections import defaultdict

from express_anal_app.demo_database import fill_denser_anal_table, clean_database, fill_database
from express_anal_app.models import DenserAnal, Shift, LeachingExpressAnal, Journal, ProductionErrors, ZnPulpAnal, \
    CuPulpAnal, FeSolutionAnal, DailyAnalysis, HydroMetal, CinderDensity, Agitators
from pprint import pprint
from dateutil.parser import parse
from itertools import product


from login_app.models import Employee
from express_anal_app.models import Employee, Shift, DenserAnal
from utils.deep_dict import deep_dict


def add_model_to_dict(model, res, attrs=None):
    if attrs is None:
        attrs = [f.name for f in model._meta.get_fields(include_parents=False)]

    for attr in attrs:
        val = getattr(model, attr)
        if val is not None:
            res[attr] = val


def get_densers_table(shift=None):
    if shift is None:
        shift = Shift.objects.all()[0]

    data = DenserAnal.objects.filter(shift=shift)
    res = deep_dict()

    for d in data:
        for attr in ['ph', 'cu', 'fe', 'liq_sol']:
            res[d.time][d.point][d.sink][attr] = getattr(d, attr)

    return res.clear_empty().get_dict()


def get_leaching_express_anal_table(shift=None):
    if shift is None:
        shift = Shift.objects.all()[0]

    res = deep_dict()

    data = LeachingExpressAnal.objects.filter(shift=shift)
    for d in data:
        for attr in ['co', 'sb', 'cu', 'cu_st1', 'cd', 'solid_st1', 'ph', 'fe', 'arsenic', 'solid', 'current', 'density']:
            val = getattr(d, attr)
            if val is not None:
                res[d.time][d.point][attr] = val

    data = ProductionErrors.objects.filter(shift=shift)
    for d in data:
        for attr in ['norm', 'fact', 'error', 'correction', 'verified']:
            val = getattr(d, attr)
            if val is not None:
                res[d.time]['prod_correction'][attr] = val

    return res.clear_empty().get_dict()


def get_solutions_table(shift=None):
    if shift is None:
        shift = Shift.objects.all()[0]

    res = deep_dict()

    data = ZnPulpAnal.objects.filter(shift=shift)
    for d in data:
        for attr in ['liq_sol', 'ph', 't0']:
            val = getattr(d, attr)
            if val is not None:
                res[d.time]['zn_pulp'][attr] = val

    data = CuPulpAnal.objects.filter(shift=shift)
    for d in data:
        for attr in ['liq_sol', 'before', 'after', 'solid']:
            val = getattr(d, attr)
            if val is not None:
                res[d.time]['cu_pulp'][attr] = val

    data = FeSolutionAnal.objects.filter(shift=shift)
    for d in data:
        for attr in ['h2so4', 'solid', 'sb', 'cu', 'fe', 'density', 'arsenic', 'cl']:
            val = getattr(d, attr)
            if val is not None:
                res[d.time]['fe_sol'][attr] = val

    for i, k in enumerate(sorted(res.keys())):
        res[k]['num'] = i

    return res.clear_empty().get_dict()


def get_solutions2_table(shift=None):
    if shift is None:
        shift = Shift.objects.all()[0]
    data = DailyAnalysis.objects.filter(shift=shift)[0]

    res = {}
    for attr in ['shlippe_sb', 'activ_sas', 'circulation_denser', 'fe_hi1', 'fe_hi2']:
        val = getattr(data, attr)
        if val is not None:
            res[attr] = val
    return res


def get_hydrometal1_table(shift=None):
    if shift is None:
        shift = Shift.objects.all()[0]

    res = deep_dict()
    for d in HydroMetal.objects.filter(shift=shift):
        add_model_to_dict(d, res[d.time][str(d.mann_num)])

    return res.clear_empty().get_dict()


def get_cinder_gran_table(shift=None):
    if shift is None:
        shift = Shift.objects.all()[0]

    res = deep_dict()
    data = CinderDensity.objects.filter(shift=shift)[0]
    for attr in ['gran_avg', 'fe_avg', 'fe_shave']:
        val = getattr(data, attr)
        if val is not None:
            res[attr] = val

    for d in CinderDensity.objects.filter(shift=shift):
        add_model_to_dict(d, res['grans'][d.time], attrs=['gran'])

    return res.clear_empty().get_dict()


def get_agitators_table(shift=None):
    if shift is None:
        shift = Shift.objects.all()[0]

    res = deep_dict()
    for d in Agitators.objects.filter(shift=shift):
        add_model_to_dict(d, res['times'][d.time][d.num][d.before])

    res['comment'] = Agitators.objects.filter(shift=shift)[0]

    for d in CinderDensity.objects.filter(shift=shift):
        add_model_to_dict(d, res['grans'][d.time], attrs=['gran'])

    return res.clear_empty().get_dict()


# this method can be called by typing "python manage.py my_command"
def command_to_process():
    clean_database()
    fill_database()

    a = get_agitators_table()
    pprint(a)