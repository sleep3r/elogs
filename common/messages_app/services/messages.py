from login_app.models import Employee
from common.messages_app.models import Message
from common.all_journals_app.models import CellValue

def get_addressees(all=False, positions=None, ids=None, plant=None):
    '''Отдает список адресатов'''
    res = []
    if all:
        return Employee.objects.only('user')
    if positions:
        for p in positions:
            emp = Employee.objects.filter(plant=plant, position=p)
            res.extend(emp)
    if ids:
        for id in ids:
            emp = Employee.objects.get(id=id)
            res.append(emp)

    return res


def filter_or_none(model, *args, **kwargs):
    try:
        return model.objects.filter(*args, **kwargs)
    except model.DoesNotExist:
        return None


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None
