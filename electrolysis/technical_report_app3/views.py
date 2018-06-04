from django.shortcuts import render

from django.shortcuts import render
from utils.deep_dict import deep_dict

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from utils.deep_dict import deep_dict
from datetime import time

# Create your views here.
from django.template import loader

# from common.all_journals_app.models import JournalPage
from common.all_journals_app.services.context_creator import get_common_context



@login_required
def index(request):
    context = get_common_context(journal_name="electrolysis_technical_report_3_degree")
    template = loader.get_template('common.html')

    left_table = deep_dict()
    right_table = deep_dict()

    left_table.title = "Левая таблица"
    left_table.name = "technical_report3_tables/left_table.html"

    right_table.title = "Правая таблица"
    right_table.name = "technical_report3_tables/right_table.html"

    context.tables = [left_table, right_table]
    return HttpResponse(template.render(context, request))
