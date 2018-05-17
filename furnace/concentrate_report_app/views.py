from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from utils.deep_dict import deep_dict

# Create your views here.
from django.template import loader

from common.all_journals_app.models import JournalPage
from common.all_journals_app.services.context_creator import get_common_context


@login_required
def index(request):
    context = {}
    template = loader.get_template('common.html')
    return HttpResponse(template.render(context, request))


@login_required
def tpp(request):
    context = get_common_context(JournalPage.objects.all()[0])
    big_table = deep_dict()
    small_table = deep_dict()
    big_table.title = "Большая таблица"
    big_table.name = 'tables/big_table.html'
    small_table.title = "Маленькая таблица"
    small_table.name = 'tables/small_table.html'

    context.tables = [big_table, small_table]

    template = loader.get_template('common.html')
    return HttpResponse(template.render(context.get_dict(), request))
