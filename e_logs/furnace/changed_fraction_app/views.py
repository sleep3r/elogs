from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from utils.deep_dict import deep_dict
from e_logs.common.all_journals_app.services.context_creator import get_common_context


@login_required
def index(request):
    context = get_common_context(journal_name="furnace_changed_fraction", request=request)
    context.journal_title = "Рабочий журнал изменения фракции"

    main_table = deep_dict()
    main_table.name = "furnace_changed_fraction/main_table.html"

    context.tables = [
                main_table,
                ]
    template = loader.get_template('common.html')
    return HttpResponse(template.render(context, request))
