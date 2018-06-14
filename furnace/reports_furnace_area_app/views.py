# reports_furnace_area

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from utils.deep_dict import deep_dict
from django.template import loader
from common.all_journals_app.models import JournalPage
from common.all_journals_app.services.context_creator import get_common_context


@login_required
def index(request):
    context = get_common_context(journal_name="reports_furnace_area", request=request)
    template = loader.get_template('common.html')

    main_table = deep_dict()
    main_table.title = "Печной участок"
    main_table.name = "reports_furnace_area/main_table.html"

    area_class_cinder = deep_dict()
    area_class_cinder.title = "Участок классификаци огарка"
    area_class_cinder.name = "reports_furnace_area/area_class_cinder.html"

    electrofilter = deep_dict()
    electrofilter.title = "Участок электрофильтров"
    electrofilter.name = "reports_furnace_area/electrofilter.html"

    warehouse_concentrates = deep_dict()
    warehouse_concentrates.title = "Склад концентратов"
    warehouse_concentrates.name = "reports_furnace_area/warehouse_concentrates.html"

    airmachines = deep_dict()
    airmachines.title = "Участок воздуховных машин"
    airmachines.name = "reports_furnace_area/airmachines.html"

    constraints_table = deep_dict()
    constraints_table.title = "Ограничения"
    constraints_table.name = "reports_furnace_area/constraints_table.html"

    context.tables = [
        main_table,
        area_class_cinder,
        electrofilter,
        warehouse_concentrates,
        airmachines,

    ]

    return HttpResponse(template.render(context, request))
