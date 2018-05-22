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
    context = get_common_context(journal_name="report_income_outcome_schieht")

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
        mode = 'plan'  # 'plan'

    context.mode = mode
    # context.main_table_id = 'main_table_' + mode + '_' + str(selected_date)
    # context.supply_zinc_table_id = 'supply_zinc_table_' + mode + str(selected_date)
    context.main_table_id = 'main_table'
    context.supply_zinc_table_id = 'supply_zinc_table'

    main_table = deep_dict()
    main_table.title = "План загрузки шихты"
    main_table.name = 'tables/main_table.html'

    year_plan_schieht = deep_dict()
    year_plan_schieht.title = "Расчет годового плана шихты"
    year_plan_schieht.name = "tables/year_plan_schieht.html"

    small_plan_table = deep_dict()
    small_plan_table.title = "Какая-то таблица"
    small_plan_table.name = "tables/small_plan_table.html"

    supply_zinc_table = deep_dict()
    supply_zinc_table.title = "Поставка цинковых концентратов"
    supply_zinc_table.name = "tables/supply_of_zinc_concentrates.html"

    context.tables = [main_table,
                      year_plan_schieht,
                      small_plan_table,
                      supply_zinc_table]

    template = loader.get_template('common.html')
    return HttpResponse(template.render(context, request))
