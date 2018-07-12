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


# Create your views here.
def index(request):
    context = get_common_context(
        journal_name="electrolysis_repair_report_tables",
        page_type="equipment",
        request=request
    )
    context.journal_title = 'Журнал по ремонту оборудования'

    template = loader.get_template('common.html')

    main_table = deep_dict()
    right_table = deep_dict()

    main_table.name = "repair_app_tables/main_table.html"

    context.tables = [main_table]
    return HttpResponse(template.render(context, request))
