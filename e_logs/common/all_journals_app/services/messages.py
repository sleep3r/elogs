from e_logs.common.login_app.models import Employee
from e_logs.common.messages_app.models import Message

from utils.deep_dict import deep_dict
from utils.webutils import model_to_dict


def get_addressees(all=False, positions=None, ids=None, plant=None):
    res = []
    if all:
        return list(Employee.objects.filter(plant=plant))
    if positions:
        for p in positions:
            emp = list(Employee.objects.filter(plant=plant, position=p))
            res.extend(emp)
    if ids:
        for id in ids:
            emp = list(Employee.objects.get(id=id))
            res.append(emp)

    return res


def report_critical(model, where=None):
    fields = model.get_critical(where=where)
    if fields:
        for emp in get_addressees(all=True):
            msg = Message(type='critical_value', text=f'Критические значения в полях: {fields}', addressee=emp)
            msg.save()


def get_messages_dict(empl):
    res = []
    for m in Message.objects.filter(is_read=False, addressee=empl):
        if not m.is_read:
            res.append({
                'type': m.type,
                'message': m.text,
                'id': m.id
            })

    return res
