from collections import defaultdict
from datetime import timedelta

import environ

from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.template import loader, TemplateDoesNotExist
from django.views import View

from e_logs.common.all_journals_app.models import Shift, Journal, Plant, EquipmentGroup, YearGroup, MonthGroup
from e_logs.core.utils.webutils import logged, current_date

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env("config/settings/.env")


def get_current_group(journal):
    if journal.type == 'shift':
        number_of_shifts = Shift.get_number_of_shifts(journal)
        assert int(number_of_shifts) > 0, "<= 0 number of shifts"

        shifts = Shift.objects.cache() \
            .filter(journal=journal, date__lte=current_date()).order_by('-date', '-order')
        for shift in shifts:
            if shift.is_active():
                return shift

        assert True, "No active shifts!"
    elif journal.type == 'year':
        year = YearGroup.objects.filter(journal=journal).order_by('year').last()
        return year



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
    with open(f'templates/tables/{plant_name}/{journal_name}/{table_name}.html', 'r') as table_file:
        return HttpResponse(table_file.read())


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


class GetYears(View):
    def get(self, request, plant_name: str, journal_name: str):

        def year_event(year):
            return {
                'title': '{} год'.format(year.year),
                'url': '/{}/{}/{}/'.format(year.journal.plant.name, year.journal.name, year.id),
            }

        result = []
        plant = Plant.objects.get(name=plant_name)
        journal = Journal.objects.get(plant=plant, name=journal_name)

        if journal.type == 'year':
            years = YearGroup.objects.select_related('journal', 'journal__plant'). \
                filter(journal__name=journal_name, journal__plant__name=plant_name)
            years_dict = defaultdict(list)

            for year in years:
                years_dict[str(year.year)].append(year)

            for years in years_dict.values():
                for year in years:
                    result.append(year_event(year))

            return JsonResponse(result, safe=False)
        else:
            raise TypeError('Attempt to get years for non-year journal')
get_years = GetYears.as_view()


class GetMonths(View):
    def get(self, request, plant_name: str, journal_name: str):

        def month_event(month):
            return {
                'title': f'{month.month} {month.year} года',
                'url': '/{}/{}/{}/'.format(month.journal.plant.name, month.journal.name, month.id),
            }

        result = []
        plant = Plant.objects.get(name=plant_name)
        journal = Journal.objects.get(plant=plant, name=journal_name)

        if journal.type == 'month':
            months = MonthGroup.objects.select_related('journal', 'journal__plant'). \
                filter(journal__name=journal_name, journal__plant__name=plant_name)
            months_dict = defaultdict(list)

            for month in months:
                months_dict[str(month.month)].append(month)

            for months in months_dict.values():
                for month in months:
                    result.append(month_event(month))

            return JsonResponse(result, safe=False)
        else:
            raise TypeError('Attempt to get months for non-month journal')
get_months = GetMonths.as_view()


class GetEquipment(View):
    def get(self, request, plant_name: str, journal_name: str):

        def equipment_event(equipment):
            return {
                'title': f'{equipment.name}',
                'url': '/{}/{}/{}/'.format(equipment.journal.plant.name,
                                           equipment.journal.name,
                                           equipment.id),
            }

        result = []
        plant = Plant.objects.get(name=plant_name)
        journal = Journal.objects.get(plant=plant, name=journal_name)

        if journal.type == 'month':
            equipment = EquipmentGroup.objects.select_related('journal', 'journal__plant'). \
                filter(journal__name=journal_name, journal__plant__name=plant_name)
            equipment_dict = defaultdict(list)

            for eq in equipment:
                equipment[str(eq.name)].append(eq)

            for equipment in equipment_dict.values():
                for eq in equipment:
                    result.append(equipment_event(eq))

            return JsonResponse(result, safe=False)
        else:
            raise TypeError('Attempt to get equipment for non-equipment journal')
get_equipment = GetEquipment.as_view()