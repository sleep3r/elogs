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

    udel_table = deep_dict()
    udel_table.title = "Удельная производительность печей"
    udel_table.name = "reports_furnace_area/udel_table.html"


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
    airmachines.title = "Участок воздуходувных машин"
    airmachines.name = "reports_furnace_area/airmachines.html"

    fences_table = deep_dict()
    fences_table.title = "Ограждения"
    fences_table.name = "reports_furnace_area/fences_table.html"

    page2_table1 = deep_dict()
    page2_table1.title = "Концентрация по времени"
    page2_table1.name = "reports_furnace_area/page2_table1.html"

    page2_table2 = deep_dict()
    page2_table2.title = "Места отбора пробы"
    page2_table2.name = "reports_furnace_area/page2_table2.html"

    page2_table3 = deep_dict()
    page2_table3.title = "Корректирующие действия"
    page2_table3.name = "reports_furnace_area/page2_table3.html"

    page2_table4 = deep_dict()
    page2_table4.title = "Самоохрана"
    page2_table4.name = "reports_furnace_area/page2_table4.html"

    page2_table5 = deep_dict()
    page2_table5.title = "Мат. Тех. Ценности"
    page2_table5.name = "reports_furnace_area/page2_table5.html"

    context.tables = [
        main_table,
        udel_table,
        area_class_cinder,
        electrofilter,
        warehouse_concentrates,
        airmachines,
        fences_table,
        page2_table1,
        page2_table2,
        page2_table3,
        page2_table4,
        page2_table5,
    ]

    return HttpResponse(template.render(context, request))
