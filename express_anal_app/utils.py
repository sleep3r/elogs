import random

from dateutil.parser import parse
from itertools import product

from django.contrib.auth.models import User
from django.utils import timezone

from express_anal_app.models import Employee, Shift, DenserAnal


def fill_database():
    laborant = Employee.objects.get(user__username='pupkin')
    master = Employee.objects.get(user__username='abdul')

    shift = Shift(order=1, master=master, laborant=laborant, plant='leaching', date=parse('07.01.2017')).save()

    times = [parse('07.01.2017 10:00:00'), parse('07.01.2017 12:00:00'), parse('07.01.2017 18:00:00')]
    sinks = ['lower', 'upper']
    points = ['10', '11', '12']

    for t, s, p in product(times, sinks, points):
        da = DenserAnal(shift=shift, time=t, sink=p, point=p)
        for attr in ['ph', 'cu', 'fe', 'liq_sol']:
            setattr(da, attr, random.uniform(0, 100))
        da.save()