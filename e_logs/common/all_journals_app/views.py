from collections import defaultdict
from datetime import timedelta

import environ
from cacheops import cached_as, invalidate_obj, invalidate_model

from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import render_to_response
from django.template import loader, TemplateDoesNotExist
from django.views import View

from e_logs.common.all_journals_app.models import Shift, Journal, Plant
from e_logs.common.login_app.models import Employee
from e_logs.core.utils.webutils import logged, current_date

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env("config/settings/.env")


def get_current_shift(journal):
    number_of_shifts = Shift.get_number_of_shifts(journal)
    assert int(number_of_shifts) > 0, "<= 0 number of shifts"

    shifts = Shift.objects.cache() \
        .filter(journal=journal, date__lte=current_date()).order_by('-date', '-order')
    for shift in shifts:
        if shift.is_active:
            return shift

    assert True, "No active shifts!"


@logged
def permission_denied(request, exception, template_name='errors/403.html') -> HttpResponse:
    """ View for action with denied permission """
    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        return HttpResponseForbidden('<h1>403 Forbidden</h1>', content_type='text/html')
    return HttpResponseForbidden(
        template.render(request=request, context={'exception': str(exception)}))


def get_table_template(request, plant_name, journal_name, table_name):
    return render_to_response(f'tables/{plant_name}/{journal_name}/{table_name}.html')


class GetShifts(View):
    def get(self, request, plant_name: str, journal_name: str,
            from_date=current_date() - timedelta(days=30),
            to_date=current_date()):
        """Creates shifts for speficied period of time"""

        def shift_event(shift, is_owned):
            return {
                'title': '{} смена'.format(shift.order),
                'start': shift.start_time,
                'url': '/{}/{}/{}/'.format(shift.journal.plant.name, shift.journal.name, shift.id),
                'color': '#169F85' if is_owned else '#2A3F54'
            }

        result = []
        user = request.user
        plant = Plant.objects.get(name=plant_name)
        journal = Journal.objects.get(plant=plant, name=journal_name)
        employee = user.employee
        # invalidate_model(Shift)
        owned_shifts = employee.shift_set.all()

        if journal.type == 'shift':
            shifts = Shift.objects.select_related('journal', 'journal__plant'). \
                filter(date__range=[from_date, to_date + timedelta(days=1)],
                       journal__name=journal_name,
                       journal__plant__name=plant_name)
            shifts_dict = defaultdict(list)

            for shift in shifts:
                shifts_dict[str(shift.date)].append(shift)

            for shifts in shifts_dict.values():
                for shift in shifts:
                    is_owned = shift in owned_shifts
                    result.append(shift_event(shift, is_owned))

            return JsonResponse(result, safe=False)
        else:
            raise TypeError('Attempt to get shifts for non-shift journal')


get_shifts = GetShifts.as_view()
