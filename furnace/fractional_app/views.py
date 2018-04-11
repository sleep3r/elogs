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

    for o in MeasurementPair.objects.all():
        res['data'][o.id]['cinder']['time'] = o.cinder.user_time
        res['data'][o.id]['cinder']['masses'] = [w.mass for w in o.cinder.weights.all()]
        res['data'][o.id]['cinder']['min_sizes'] = [w.min_size for w in o.cinder.weights.all()]

        res['data'][o.id]['schieht']['time'] = o.schieht.user_time
        res['data'][o.id]['schieht']['masses'] = [w.mass for w in o.schieht.weights.all()]
        res['data'][o.id]['schieht']['min_sizes'] = [w.min_size for w in o.schieht.weights.all()]

    return res