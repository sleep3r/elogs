import json
from collections import defaultdict
from datetime import timedelta

import environ
import os

from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.template import loader, TemplateDoesNotExist
from django.utils import timezone
from django.views import View

from e_logs.common.all_journals_app.models import Shift, Journal, Plant, Equipment, Year, Month
from e_logs.core.utils.webutils import logged, current_date
from e_logs.core.views import LoginRequired

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(".env")


def _get_current_group(journal):
    if journal.type == 'shift':
        shifts = Shift.objects.filter(journal=journal, date__lte=current_date()).order_by('-date', 'order')
        print(timezone.localtime())
        for shift in shifts:
            print(shift.is_active(timezone.localtime()))
            if shift.is_active(timezone.localtime()):
                return shift

    elif journal.type == 'year':
        year = Year.objects.get(journal=journal, year_date=current_date().year)
        return year

    elif journal.type == 'month':
        month = Month.objects.get(journal=journal,
                                  month_order=current_date().month,
                                  year_date=current_date().year)
        return month

    else:
        return Equipment.objects.filter(journal=journal).first()


@logged
def permission_denied(request, exception, template_name='errors/403.html') -> HttpResponse:
    """ View for action with denied permission """
    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        return HttpResponseForbidden('<h1>403 Forbidden</h1>', content_type='text/html')
    return HttpResponseForbidden(
        template.render(request=request, context={'exception': str(exception)}))


def get_table_template(request):
    plant_name = request.GET.get("plant_name", None)
    journal_name = request.GET.get("journal_name", None)
    table_name = request.GET.get("table_name", None)
    version = request.GET.get("version", None)

    if plant_name is None:
        plant_name = Journal.objects.get(name=journal_name).plant.name
    if version is None:
        version = len(os.listdir(f'templates/tables/{plant_name}/{journal_name}/'))


    with open(f'templates/tables/{plant_name}/{journal_name}/v{version}/{table_name}.html', 'r') as table_file:
        return HttpResponse(table_file.read())

class GetGroups(LoginRequired, View):
    def get(self, request, plant_name: str, journal_name: str):
        user = request.user
        plant = Plant.objects.get(name=plant_name)
        journal = Journal.objects.get(plant=plant, name=journal_name)

        if journal.type == 'shift':
            return self.get_shifts(user, journal)

        elif journal.type == 'year':
            return self.get_years(user, journal)

        elif journal.type == 'month':
            return self.get_months(user, journal)

        else:
            return self.get_equipment(user, journal)

    def get_shifts(self, user, journal):
        def shift_event(shift, is_owned):
            return {
                'title': '{} смена'.format(shift.order),
                'start': shift.start_time,
                'url': '/{}/{}/{}/'.format(shift.journal.plant.name, shift.journal.name, shift.id),
                'color': '#169F85' if is_owned else '#2A3F54'
            }

        result = []
        owned_shifts = user.employee.shift_set.all()
        from_date = current_date() - timedelta(days=30)
        to_date = current_date()

        if journal.type == 'shift':
            shifts = Shift.objects.select_related('journal', 'journal__plant').only('order'). \
                filter(date__range=[from_date, to_date + timedelta(days=1)], journal=journal).cache()
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

    def get_years(self, user, journal):
        def year_event(year):
            return {
                'id': year.id,
                'title': '{}-й год'.format(year.year_date),
                'url': '/{}/{}/{}/'.format(year.journal.plant.name, year.journal.name, year.id),
            }

        result = []

        if journal.type == 'year':
            years = Year.objects.select_related('journal', 'journal__plant').only('year_date'). \
                filter(journal=journal, year_date__lte=current_date().year). \
                cache().order_by('-year_date')
            years_dict = defaultdict(list)

            for year in years:
                years_dict[str(year.year)].append(year)

            for years in years_dict.values():
                for year in years:
                    result.append(year_event(year))

            return JsonResponse(result, safe=False)
        else:
            raise TypeError('Attempt to get years for non-year journal')

    def get_months(self, user, journal):
        def month_event(month):
            return {
                'id': month.id,
                'year': f'{month.year_date}-й год',
                'month': f'{month.month_date}',
                'url': '/{}/{}/{}/'.format(month.journal.plant.name, month.journal.name, month.id),
            }

        result = []

        if journal.type == 'month':
            months = Month.objects.select_related('journal', 'journal__plant'). \
                filter(journal=journal, year_date__lte=current_date().year).cache() \
                .order_by('-year_date')
            months_dict = defaultdict(list)

            for month in months:
                months_dict[str(month.month)].append(month)

            for months in months_dict.values():
                for month in months:
                    result.append(month_event(month))

            return JsonResponse(result, safe=False)
        else:
            raise TypeError('Attempt to get months for non-month journal')

    def get_equipment(self, user, journal):
        def equipment_event(equipment):
            return {
                'id': equipment.id,
                'title': f'{equipment.name}',
                'url': '/{}/{}/{}/'.format(equipment.journal.plant.name,
                                           equipment.journal.name,
                                           equipment.id),
            }

        result = []

        if journal.type == 'equipment':
            equipment = Equipment.objects.select_related('journal', 'journal__plant').filter(journal=journal).cache()
            equipment_dict = defaultdict(list)

            for eq in equipment:
                equipment_dict[str(eq.name)].append(eq)

            for equipment in equipment_dict.values():
                for eq in equipment:
                    result.append(equipment_event(eq))

            return JsonResponse(result, safe=False)
        else:
            raise TypeError('Attempt to get equipment for non-equipment journal')


get_groups = GetGroups.as_view()
