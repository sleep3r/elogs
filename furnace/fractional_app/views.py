from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from furnace.fractional_app.models import *
from utils.deep_dict import deep_dict
from django.http import HttpResponse, JsonResponse
from django.template import loader

from utils.webutils import process_json_view
@login_required
def index(request):
    template = loader.get_template('spa-index.html')
    return HttpResponse(template.render())


@process_json_view(auth_required=False)
def granularity_object(request):
    res = deep_dict()

    for o in MeasurementPair.objects.all()[:2]:
        res['data'][o.id+1234]['cinder']['time'] = o.cinder.user_time + timedelta(days=700)
        res['data'][o.id+1234]['cinder']['masses'] = [float(w.mass) for w in o.cinder.weights.all()]
        res['data'][o.id+1234]['cinder']['min_sizes'] = [float(w.min_size) for w in o.cinder.weights.all()]

        res['data'][o.id+1234]['schieht']['time'] = o.schieht.user_time + timedelta(days=700)
        res['data'][o.id+1234]['schieht']['masses'] = [float(w.mass) for w in o.schieht.weights.all()]
        res['data'][o.id+1234]['schieht']['min_sizes'] = [float(w.min_size) for w in o.schieht.weights.all()]


    for o in MeasurementPair.objects.all():
        res['data'][o.id]['cinder']['time'] = o.cinder.user_time
        res['data'][o.id]['cinder']['masses'] = [float(w.mass) for w in o.cinder.weights.all()]
        res['data'][o.id]['cinder']['min_sizes'] = [float(w.min_size) for w in o.cinder.weights.all()]

        res['data'][o.id]['schieht']['time'] = o.schieht.user_time
        res['data'][o.id]['schieht']['masses'] = [float(w.mass) for w in o.schieht.weights.all()]
        res['data'][o.id]['schieht']['min_sizes'] = [float(w.min_size) for w in o.schieht.weights.all()]

    return res


@process_json_view(auth_required=False)
def granularity_gaphs(request):
    def get_mean(masses, sizes):
        msum = sum(masses)
        mass_parts = [m/msum for m in masses]
        sizes = sizes + [sizes[-1]]
        middles = [(sizes[i] + sizes[i+1])/2 for i in range(len(sizes)-1)]
        res = [float(mas)*float(mid) for mas, mid in zip(mass_parts, middles)]
        return sum(res)

    cinders = []
    schieht = []

    for o in MeasurementPair.objects.all():
        masses = [w.mass for w in o.cinder.weights.all()]
        min_sizes = [w.min_size for w in o.cinder.weights.all()]
        cinders.append([o.cinder.user_time, get_mean(masses, min_sizes)])

        masses = [w.mass for w in o.schieht.weights.all()]
        min_sizes = [w.min_size for w in o.schieht.weights.all()]
        schieht.append([o.schieht.user_time, get_mean(masses, min_sizes)])

    res = deep_dict()
    res['data']['cinder'] = cinders
    res['data']['schieht'] = schieht

    return res