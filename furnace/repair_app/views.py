import pprint

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

from common.all_journals_app.fields_descriptions.fields_info import fields_info_desc
from utils.deep_dict import deep_dict

from common.all_journals_app.models import JournalPage
from common.all_journals_app.services.context_creator import get_common_context



@login_required
def index(request):
    context = get_common_context(journal_name="furnace_repair", request=request)
    context.journal_title = 'Журнал по ремонту'

    repair_table = deep_dict()
    repair_table.title = "Ремонты по Обжиговому цеху"
    repair_table.name = "furnace_repair/repair.html"

    context.tables = [
                       repair_table,
                      ]

    template = loader.get_template('common.html')
    return HttpResponse(template.render(context, request))
