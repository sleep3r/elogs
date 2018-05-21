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
    context = get_common_context(journal_name="svodka_income_outcome_shihta")

    main_table = deep_dict()
    main_table.title = "План загрузки шихты"
    main_table.name = 'tables/main_table.html'

    if 'month' in request.GET:
        selected_date = request.GET['month']
        current_date = selected_date.split('-')
        if 1 in current_date:
            month = current_date[1]
        else:
            month = 5
        context.selected_month = selected_date
    else:
        selected_date = '2018-05'

    if 'mode' in request.GET:
        mode = request.GET['mode']
    else:
        mode = 'fact'  # 'plan'


    context.mode = mode
    context.table_id = 'main_table_' + mode + '_'+ str(selected_date)

    if context.table_id in context.full_data:
        context.needNewLine = True
    else:
        context.needNewLine = False

    context.dump = pprint.pformat(context.full_data, indent=4)
    context.tables = [main_table]
    template = loader.get_template('common.html')
    return HttpResponse(template.render(context, request))
