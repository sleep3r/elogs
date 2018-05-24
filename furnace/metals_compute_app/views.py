import pprint

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from utils.deep_dict import deep_dict

from common.all_journals_app.models import JournalPage
from common.all_journals_app.services.context_creator import get_common_context



# Create your views here.
@login_required
def index(request):
    context = get_common_context(journal_name="metals_compute")

    main_table = deep_dict()
    main_table.title = "Среднее содержание за месяц"
    main_table.name = 'metals_compute/main_table.html'

    sns_table = deep_dict()
    sns_table.title = "СНС"
    sns_table.name = "metals_compute/sns_table.html"

    context.tables = [
                       main_table,
                       sns_table
                      ]

    template = loader.get_template('common.html')
    return HttpResponse(template.render(context, request))
