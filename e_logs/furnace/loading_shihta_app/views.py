import pprint
from datetime import date
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from e_logs.core.utils.deep_dict import deep_dict

from e_logs.common.all_journals_app.models import JournalPage
from e_logs.common.all_journals_app.services.context_creator import get_common_context


@login_required
def index(request):
    context = get_common_context(journal_name="report_income_outcome_schieht", page_type='year', request=request)
    context.journal_title = 'Поступление, расходы и остатки Zn концентратов'

    context.main_table_id = 'main_table'
    context.supply_zinc_table_id = 'supply_zinc_table'
    context.summary_table_id = 'summary_table'

    main_table = deep_dict()
    main_table.name = 'tables/main_table.html'

    year_plan_schieht = deep_dict()
    year_plan_schieht.name = "tables/year_plan_schieht.html"

    small_plan_table = deep_dict()
    small_plan_table.name = "tables/small_plan_table.html"

    supply_zinc_table = deep_dict()
    supply_zinc_table.name = "tables/supply_of_zinc_concentrates.html"

    summary_table = deep_dict()
    summary_table.name = "tables/summary_table.html"

    context.months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    months_ru = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    context.months_trans = dict(zip(context.months, months_ru))
    context.plan_or_fact = ['plan', 'fact']
    context.date_year = datetime.now().year
    context.cur_month = context.months[date.today().month-1]

    context.tables = [
                      main_table,
                      year_plan_schieht,
                      # small_plan_table,
                      supply_zinc_table,
                      summary_table
                      ]

    template = loader.get_template('common.html')
    return HttpResponse(template.render(context, request))
