# buff_journal

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from utils.deep_dict import deep_dict
from django.template import loader
from common.all_journals_app.models import JournalPage
from common.all_journals_app.services.context_creator import get_common_context


@login_required
def index(request):
    context = get_common_context(journal_name="buff_journal", request=request)
    context.journal_title = "Журнал для проверки"

    template = loader.get_template('common.html')

    trening_table = deep_dict()
    trening_table.title = "проверочная"
    trening_table.name = "buffering_app/trening_table.html"

    context.tables = [trening_table]
    return HttpResponse(template.render(context, request))
