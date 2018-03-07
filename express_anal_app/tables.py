import random
from collections import defaultdict

from express_anal_app.demo_database import fill_denser_anal_table, clean_database, fill_database
from express_anal_app.models import DenserAnal, Shift, LeachingExpressAnal, Journal, ProductionErrors, ZnPulpAnal, \
    CuPulpAnal, FeSolutionAnal, DailyAnalysis
from pprint import pprint
from dateutil.parser import parse
from itertools import product


from login_app.models import Employee
from express_anal_app.models import Employee, Shift, DenserAnal
from utils.deep_dict import deep_dict


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

    data = DailyAnalysis.objects.filter(shift=shift)
    for d in data:
        for attr in ['shlippe_sb', 'activ_sas', 'circulation_denser', 'fe_hi1', 'fe_hi2']:
            val = getattr(d, attr)
            if val is not None:
                res[d.time]['daily'][attr] = val

    return res.clear_empty().get_dict()




# this method can be called by typing "python manage.py my_command"
def command_to_process():
    clean_database()
    fill_database()

    a = get_solutions_table()
    pprint(a)