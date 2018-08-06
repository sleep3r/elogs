from datetime import date, timedelta

from e_logs.core.utils.webutils import process_json_view, logged
from e_logs.common.all_journals_app.models import Shift, Plant, Journal


def shift_event(request, shift, is_owned):
    return {
        'title': '{} смена'.format(shift.order),
        'start': shift.start_time,
        'url': '?id={}'.format(shift.id),
        'title:': 'Some title',
        'color': '#169F85' if is_owned else '#2A3F54'
    }


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


@logged
@process_json_view(auth_required=False)
def get_shifts(request, plant_name, journal_name,
               from_date=date.today()-timedelta(days=30),
               to_date=date.today()):
    """Creates shifts for speficied period of time"""
    result = []
    plant = Plant.objects.get(name=plant_name)
    journal = Journal.objects.get(plant=plant, name=journal_name)
    employee = request.user.employee
    if journal.type == 'shift':
        number_of_shifts = Shift.get_number_of_shifts(journal)
        for shift_date in daterange(from_date, to_date):
            for shift_order in range(1, number_of_shifts+1):
                shift = Shift.objects.get_or_create(
                    journal=journal,
                    order=shift_order,
                    date=shift_date
                )[0]
                is_owned = employee in shift.employee_set.all()
                result.append(shift_event(request, shift, is_owned))
        return result
    else:
        raise TypeError('Attempt to get shifts for non-shift journal')
