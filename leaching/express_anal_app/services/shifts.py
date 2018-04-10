import datetime

from django.utils import timezone

from leaching.express_anal_app.models import Shift
from utils.deep_dict import deep_dict


def create_shifts_for_month():
    today = timezone.now().date()
    for i in range(30):
        d = today - datetime.timedelta(days=1*i)
        Shift.objects.get_or_create(date=d, order=1)
        Shift.objects.get_or_create(date=d, order=2)


def get_editable_shifts(employee):
    create_shifts_for_month()

    cur_order = 1 if (8 <= timezone.now().hour < 20) else 2
    today = timezone.now().date()
    month_ago = timezone.now().date() - datetime.timedelta(days=30)
    Shift.objects.filter(date__gte=month_ago)

    if employee.position == 'laborant':
        own = list(employee.leaching_labornat_shifts.filter(date__gte=month_ago))
    elif employee.position == 'master':
        own = list(employee.leaching_master_shifts.filter(date__gte=month_ago))
    elif employee.position == 'hydro':
        own = list(employee.leaching_hydro_shifts.filter(date__gte=month_ago))
    else:
        own = []

    empty = list(Shift.objects.filter(date__gte=month_ago, **{employee.position + '__isnull': True}))
    if cur_order == 1:
        empty = list(filter(lambda x: x.date != today or x.order!=2, empty))
        own = list(filter(lambda x: x.date != today or x.order!=2, own))

    res = {
        'own': own,
        'empty': empty
    }

    return res
