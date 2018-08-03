import json
from datetime import timedelta

from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template import loader
from functional import seq

from e_logs.common.all_journals_app.models import Cell, Shift, Plant, Measurement
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
            measurement = Measurement.objects.create(type="measurement", time=timezone.now(), name="fractional_anal",
                                                     plant=Plant.objects.get(name="furnace")).id

        for m_value in req['cinder']['masses']:
            Cell.objects.create(table_name="measurements", field_name='cinder_mass',
                                index=0, value=m_value, group_id=measurement)
        for m_value in req['cinder']['min_sizes']:
            Cell.objects.create(table_name="measurements", field_name='cinder_size',
                                index=0, value=m_value, group_id=measurement)
        for m_value in req['schieht']['masses']:
            Cell.objects.create(table_name="measurements", field_name='schieht_mass',
                                index=0, value=m_value, group_id=measurement)
        for m_value in req['schieht']['min_sizes']:
            Cell.objects.create(table_name="measurements", field_name='schieht_size',
                                index=0, value=m_value, group_id=measurement)

        return HttpResponse(status=201)
    return HttpResponse(status=405)


@process_json_view(auth_required=False)
def granularity_object(request):
    res = deep_dict()

    for measurement in Measurement.objects.filter(type="measurement")[:2]:
        res['data'][measurement.id + 100]['cinder']['time'] = (measurement.time + timedelta(days=700)).timestamp()
        res['data'][measurement.id + 100]['cinder']['masses'] = [round(float(m.value), 2) for m in
                                                                 Cell.objects.filter(field_name="cinder_mass",
                                                                                     group=measurement)]
        res['data'][measurement.id + 100]['cinder']['min_sizes'] = [round(float(m.value), 2) for m in
                                                                    Cell.objects.filter(field_name="cinder_size",
                                                                                        group=measurement)]

        res['data'][measurement.id + 100]['schieht']['time'] = (measurement.time + timedelta(days=700)).timestamp()
        res['data'][measurement.id + 100]['schieht']['masses'] = [round(float(m.value), 2) for m in
                                                                  Cell.objects.filter(field_name="schieht_mass",
                                                                                      group=measurement)]
        res['data'][measurement.id + 100]['schieht']['min_sizes'] = [round(float(m.value), 2) for m in
                                                                     Cell.objects.filter(field_name="schieht_size",
                                                                                         group=measurement)]

    for measurement in Measurement.objects.filter(type="measurement"):
        res['data'][measurement.id]['cinder']['time'] = measurement.time.timestamp()
        res['data'][measurement.id]['cinder']['masses'] = [round(float(m.value), 2) for m in
                                                           Cell.objects.filter(field_name="cinder_mass",
                                                                               group=measurement)]
        res['data'][measurement.id]['cinder']['min_sizes'] = [round(float(m.value), 2) for m in
                                                              Cell.objects.filter(field_name="cinder_size",
                                                                                  group=measurement)]

        res['data'][measurement.id]['schieht']['time'] = measurement.time.timestamp()
        res['data'][measurement.id]['schieht']['masses'] = [round(float(m.value), 2) for m in
                                                            Cell.objects.filter(field_name="schieht_mass",
                                                                                group=measurement)]
        res['data'][measurement.id]['schieht']['min_sizes'] = [round(float(m.value), 2) for m in
                                                               Cell.objects.filter(field_name="schieht_size",
                                                                                   group=measurement)]

    return res


@process_json_view(auth_required=False)
def granularity_graphs(request):
    def get_mean(masses, sizes):
        msum = sum(masses)
        if msum == 0:
            return 0

        mass_parts = [m / msum for m in masses]
        sizes = sizes + [sizes[-1]]
        middles = [(sizes[i] + sizes[i + 1]) / 2 for i in range(len(sizes) - 1)]
        res = [float(mas) * float(mid) for mas, mid in zip(mass_parts, middles)]
        return sum(res)

    cinders = []
    schieht = []

    cinder_masses = list(Cell.objects.filter(field_name="cinder_mass"))
    cinder_sizes = list(Cell.objects.filter(field_name="cinder_size"))
    schieht_masses = list(Cell.objects.filter(field_name="schieht_mass"))
    schieht_sizes = list(Cell.objects.filter(field_name="schieht_size"))

    for measurement in Measurement.objects.prefetch_related('cell_set').filter(type="measurement"):
        process = lambda x: seq(x).where(lambda y: y.group == measurement).map(lambda z: float(z.value)).to_list()
        masses = process(cinder_masses)
        min_sizes = process(cinder_sizes)
        cinders.append([measurement.time.timestamp(), get_mean(masses, min_sizes)])

        masses = process(schieht_masses)
        min_sizes = process(schieht_sizes)
        schieht.append([measurement.time.timestamp(), get_mean(masses, min_sizes)])

    res = deep_dict()
    res['data']['cinder'] = cinders
    res['data']['schieht'] = schieht

    return res
