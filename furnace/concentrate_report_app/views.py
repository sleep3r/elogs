from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template import loader

from common.all_journals_app.services.context_creator import get_common_context


@login_required
def index(request):
    context = {}
    template = loader.get_template('common.html')
    return HttpResponse(template.render(context, request))


@login_required
def tpp(request):
    context = get_common_context()
    template = loader.get_template('common.html')
    return HttpResponse(template.render(context, request))