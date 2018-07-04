from datetime import date, timedelta

from utils.webutils import process_json_view
from common.all_journals_app.models import JournalPage, Plant


def shift_event(request, journal_page, is_owned):

    return {
        'title': '{} смена'.format(journal_page.shift_order),
        'start': journal_page.shift_start_time,
        'url': '?id={}'.format(journal_page.id),
        'title:': 'Some title',
        'color': '#169F85' if is_owned else '#2A3F54'
    }


@process_json_view(auth_required=False)
def get_shifts(request, plant, journal_name):
    result = []
    plant = Plant.objects.get(name=plant)
    employee = request.user.employee
    recent_pages = JournalPage.objects.filter(plant=plant,
                                              journal_name=journal_name,
                                              shift_date__gte=date.today() - timedelta(days=30))

    today = date.today()
    for day in range(30):
        for shift_order in range(1, plant.number_of_shifts + 1):
            shift_date = today - timedelta(day)
            page = recent_pages.filter(shift_order=shift_order, shift_date=shift_date).first()
            if not page:
                page = JournalPage(shift_date=shift_date,
                                   shift_order=shift_order,
                                   plant=plant,
                                   journal_name=journal_name,
                                   type='shift')
                page.save()
            is_owned = employee in page.employee_set.all()
            result.append(shift_event(request, page, is_owned))

    return result
