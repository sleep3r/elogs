import datetime

from leaching.express_anal_app.services.shifts import get_editable_shifts
from utils.webutils import process_json_view


def shift_event(shift, color=None):
    res = {
        'title': f'{shift.order} смена',
        'start': datetime.datetime(shift.date.year, shift.date.month, shift.date.day, (8 if shift.order == 1 else 20)),
        'url': f'/leaching/edit/wizard?shift={shift.id}',
        'title:': 'Some title'
    }

    if color:
        res['color'] = color

    return res


@process_json_view(auth_required=False)
def accessible_shifts(request):
    empl = request.user.employee
    esh = get_editable_shifts(empl)
    own = esh['own']
    empty = esh['empty']

    res = [shift_event(shift=s, color='#169F85') for s in own] + [shift_event(shift=s, color='#2A3F54') for s in empty]

    return res