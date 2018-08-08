# repair_reports

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from e_logs.core.utils.deep_dict import deep_dict
from django.template import loader
from e_logs.common.all_journals_app.models import Shift
# from e_logs.common.all_journals_app.services.context_creator import get_common_context
from e_logs.core.utils.webutils import logged


# @logged
# @login_required
# def index(request):
#     context = get_common_context(name="leaching_repair_equipment", request=request)
#     context.journal_title = "Журнал ремонта"
#     template = loader.get_template('common.html')
#
#     left = deep_dict()
#     left.name = "repair_reports/repair_table.html"
#
#     context.tables = [left]
#     return HttpResponse(template.render(context, request))
