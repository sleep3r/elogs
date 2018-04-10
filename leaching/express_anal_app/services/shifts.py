import datetime

from django.utils import timezone

from leaching.express_anal_app.models import Shift
from utils.deep_dict import deep_dict


def get_editable_shifts(employee):
    cur_order = 1 if (8 <= timezone.now().hour < 20) else 2

    if employee.position == 'laborant':
        own = list(employee.leaching_labornat_shifts.all())
    elif employee.position == 'master':
        own = list(employee.leaching_master_shifts.all())
    elif employee.position == 'hydro':
        own = list(employee.leaching_hydro_shifts.all())
    else:
        own = []

    empty = Shift.objects.filter(**{employee.position + '__isnull': True})

    today = timezone.now().date()
    if cur_order == 2:
        current = Shift.objects.filter(date=today)
    else:
        current = Shift.objects.filter(date=today - datetime.timedelta(days=1))

    res = {}
    res['current'] = [(s.date, s.order) for s in current]
    res['own'] = [(s.date, s.order) for s in own]
    res['empty'] = [(s.date, s.order) for s in empty]

    return res
