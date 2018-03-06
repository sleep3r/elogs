import random
from collections import defaultdict

from express_anal_app.models import DenserAnal, Shift
from pprint import pprint
from dateutil.parser import parse
from itertools import product


from login_app.models import Employee
from express_anal_app.models import Employee, Shift, DenserAnal
from utils.test import deep_dict


def get_densers_table(shift=None):
    if shift is None:
        shift = Shift.objects.all()[0]

    data = DenserAnal.objects.filter(shift=shift)
    res = deep_dict()

    for d in data:
        for attr in ['ph', 'cu', 'fe', 'liq_sol']:
            res[d.time][d.point][d.sink][attr] = getattr(d, attr)

    return res


def fill_database():
    # laborant = Employee.objects.get(user__username='pupkin')
    # master = Employee.objects.get(user__username='abdul')

    shift = Shift.objects.all()[0]

    times = [parse('07.01.2017 10:00:00'), parse('07.01.2017 12:00:00'), parse('07.01.2017 18:00:00')]
    sinks = ['НС', 'ВС']
    points = ['10', '11', '12']

    for t, s, p in product(times, sinks, points):
        da = DenserAnal(shift=shift, time=t, sink=s, point=p)
        for attr in ['ph', 'cu', 'fe', 'liq_sol']:
            setattr(da, attr, random.uniform(0, 100))
        da.save()


# this method can be called by typing "python manage.py my_command
def command_to_process():
    DenserAnal.objects.all().delete()
    fill_database()
    a = get_densers_table()
    pprint(a.get_dict())