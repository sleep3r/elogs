from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template import loader

@login_required
def index(request):
    context = {}
    template = loader.get_template('common.html')
    return HttpResponse(template.render(context, request))


@login_required
def tpp(request):
    context = { "table": {"title": "dfgdfgdf", "name": "tables/tpp.html"}}
    template = loader.get_template('common.html')
    return HttpResponse(template.render(context, request))