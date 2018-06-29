# repair_reports

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from utils.deep_dict import deep_dict
from django.template import loader
from common.all_journals_app.models import JournalPage
from common.all_journals_app.services.context_creator import get_common_context


@login_required
def index(request):
    context = get_common_context(journal_name="leaching_repair_quipment", request=request)
    context.journal_title = "Журнал ремонта"
    template = loader.get_template('common.html')

    left_table = deep_dict()
    left_table.title = "Первая"
    left_table.name = "repair_reports/repair.html"

    context.tables = [left_table]
    return HttpResponse(template.render(context, request))
