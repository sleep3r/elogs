from django.shortcuts import render


from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

from e_logs.common.all_journals_app.fields_descriptions.fields_info import fields_info_desc
from utils.deep_dict import deep_dict

from e_logs.common.all_journals_app.models import JournalPage
from e_logs.common.all_journals_app.services.context_creator import get_common_context


@login_required
def index(request):
    context = get_common_context(journal_name="technological_tasks", request=request)
    context.journal_title = 'Журнал сменных производственных, тех. заданий'

    replaceable_tasks_table = deep_dict()
    replaceable_tasks_table.name = 'technologicaltasks/main_table.html'

    context.tables = [
                replaceable_tasks_table,
                  ]

    template = loader.get_template('common.html')
    return HttpResponse(template.render(context, request))
