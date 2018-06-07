# masters_raports

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from utils.deep_dict import deep_dict
from django.template import loader
from common.all_journals_app.models import JournalPage
from common.all_journals_app.services.context_creator import get_common_context


@login_required
def index(request):
    context = get_common_context(journal_name="masters_raports")
    template = loader.get_template('common.html')

    top_table = deep_dict()
    top_table.title = "Журанл рапортов мастеров смен"
    top_table.name = "masters_raports_app/top_table.html"

    seria3_table = deep_dict()
    seria3_table.title = "3-я серия"
    seria3_table.name = "masters_raports_app/seria3_table.html"

    seria4_table = deep_dict()
    seria4_table.title = "4-я серия"
    seria4_table.name = "masters_raports_app/seria4_table.html"

    params_table = deep_dict()
    params_table.title = "Параметры"
    params_table.name = "masters_raports_app/params_table.html"

    context.tables = [
        top_table,
        seria3_table,
        seria4_table,
        params_table
    ]

    last_table = deep_dict()
    last_table.title = "Последняя таблица"
    last_table.name = "masters_raports_app/last_table.html"

    context.tables = [top_table, last_table]
    return HttpResponse(template.render(context, request))
