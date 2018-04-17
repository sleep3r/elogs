from login_app.models import Message
from utils.deep_dict import deep_dict
from utils.webutils import model_to_dict


def report_critical(model, where=None):
    fields = model.get_critical()
    if fields != []:
        msg = Message(type='critical_value', position='master laborant',
                      text=f'Критические значения в полях: {fields}')
        msg.save()


def get_messages_dict():
    res = []
    for m in Message.objects.filter(is_read=False):
        if not m.is_read:
            res.append({
                'type': m.type,
                'message': m.text,
                'id': m.id
            })
    return res