import json
from datetime import timedelta

from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template import loader

from e_logs.common.all_journals_app.models import CellValue, JournalPage, Plant
from e_logs.core.utils.deep_dict import deep_dict
from e_logs.core.utils.webutils import process_json_view


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'furnace-index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['journal_title'] = 'Ситовой анализ огарка и шихты'
        return context
    

@login_required
def add_measurement(request):
    if request.method == 'POST':
        req = json.loads(request.body)

        if hasattr(req, 'id'):
            measurement = req['id']
        else:
            measurement = JournalPage.objects.create(type="measurement", time = timezone.now(), journal_name = "fractional_anal", plant=Plant.objects.get(name="furnace")).id

        for m_value in req['cinder']['masses']:
            CellValue.objects.create(table_name="measurements", field_name='cinder_mass',
                             index=0, value=m_value, journal_page_id=measurement)
        for m_value in req['cinder']['min_sizes']:
            CellValue.objects.create(table_name="measurements", field_name='cinder_size',
                             index=0, value=m_value, journal_page_id=measurement)
        for m_value in req['schieht']['masses']:
            CellValue.objects.create(table_name="measurements", field_name='schieht_mass',
                             index=0, value=m_value, journal_page_id=measurement)
        for m_value in req['schieht']['min_sizes']:
            CellValue.objects.create(table_name="measurements", field_name='schieht_size',
                             index=0, value=m_value, journal_page_id=measurement)

        return HttpResponse(status=201)
    return HttpResponse(status=405)


@process_json_view(auth_required=False)
def granularity_object(request):
    res = deep_dict()

    for measurement in JournalPage.objects.filter(type="measurement")[:2]:
        res['data'][measurement.id+100]['cinder']['time'] = (measurement.time + timedelta(days=700)).timestamp()
        res['data'][measurement.id+100]['cinder']['masses'] = [round(float(m.value), 2) for m in CellValue.objects.filter(field_name="cinder_mass", journal_page = measurement)]
        res['data'][measurement.id+100]['cinder']['min_sizes'] = [round(float(m.value), 2) for m in CellValue.objects.filter(field_name="cinder_size", journal_page = measurement)]

        res['data'][measurement.id+100]['schieht']['time'] = (measurement.time + timedelta(days=700)).timestamp()
        res['data'][measurement.id+100]['schieht']['masses'] = [round(float(m.value), 2) for m in CellValue.objects.filter(field_name="schieht_mass", journal_page = measurement)]
        res['data'][measurement.id+100]['schieht']['min_sizes'] = [round(float(m.value), 2) for m in CellValue.objects.filter(field_name="schieht_size", journal_page = measurement)]
    
    for measurement in JournalPage.objects.filter(type="measurement"):
        res['data'][measurement.id]['cinder']['time'] = measurement.time.timestamp()
        res['data'][measurement.id]['cinder']['masses'] = [round(float(m.value), 2) for m in CellValue.objects.filter(field_name="cinder_mass", journal_page = measurement)]
        res['data'][measurement.id]['cinder']['min_sizes'] = [round(float(m.value), 2) for m in CellValue.objects.filter(field_name="cinder_size", journal_page = measurement)]

        res['data'][measurement.id]['schieht']['time'] = measurement.time.timestamp()
        res['data'][measurement.id]['schieht']['masses'] = [round(float(m.value), 2) for m in CellValue.objects.filter(field_name="schieht_mass", journal_page = measurement)]
        res['data'][measurement.id]['schieht']['min_sizes'] = [round(float(m.value), 2) for m in CellValue.objects.filter(field_name="schieht_size", journal_page = measurement)]
    
    return res


@process_json_view(auth_required=False)
def granularity_graphs(request):
    def get_mean(masses, sizes):
        msum = sum(masses)
        if msum == 0:
            return 0
            
        mass_parts = [m/msum for m in masses]
        sizes = sizes + [sizes[-1]]
        middles = [(sizes[i] + sizes[i+1])/2 for i in range(len(sizes)-1)]
        res = [float(mas)*float(mid) for mas, mid in zip(mass_parts, middles)]
        return sum(res)

    cinders = []
    schieht = []

    for measurement in JournalPage.objects.filter(type="measurement"):
        masses = [float(m.value) for m in CellValue.objects.filter(field_name="cinder_mass", journal_page = measurement)]
        min_sizes = [float(m.value) for m in CellValue.objects.filter(field_name="cinder_size", journal_page = measurement)]
        cinders.append([measurement.time.timestamp(), get_mean(masses, min_sizes)])

        masses = [float(m.value) for m in CellValue.objects.filter(field_name="schieht_mass", journal_page = measurement)]
        min_sizes = [float(m.value) for m in CellValue.objects.filter(field_name="schieht_size", journal_page = measurement)]
        schieht.append([measurement.time.timestamp(), get_mean(masses, min_sizes)])

    res = deep_dict()
    res['data']['cinder'] = cinders
    res['data']['schieht'] = schieht

    return res
