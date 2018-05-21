from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from utils.deep_dict import deep_dict

from common.all_journals_app.models import JournalPage
from common.all_journals_app.services.context_creator import get_common_context



# Create your views here.
@login_required
def index(request):
    context = get_common_context(JournalPage.objects.get(journal_name="concentrate_report_journal"))

    main_table = deep_dict()
    main_table.title = "План загрузки шихты"
    main_table.name = 'tables/main_table.html'

    context.tables = [main_table]
    template = loader.get_template('common.html')
    return HttpResponse(template.render(context, request))
