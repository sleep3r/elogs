# reports_furnace_area

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from e_logs.core.utils.deep_dict import deep_dict
from django.template import loader
from e_logs.common.all_journals_app.models import JournalPage
from e_logs.common.all_journals_app.services.context_creator import get_common_context


@login_required
def index(request):
    context = get_common_context(journal_name="reports_furnace_area", request=request)
    template = loader.get_template('common.html')
    context.journal_title = "Журнал печного участка"

    main_table = deep_dict()
    main_table.name = "reports_furnace_area/main_table.html"

    udel_table = deep_dict()
    udel_table.name = "reports_furnace_area/udel_table.html"

    area_class_cinder = deep_dict()
    area_class_cinder.name = "reports_furnace_area/area_class_cinder.html"

    electrofilter = deep_dict()
    electrofilter.name = "reports_furnace_area/electrofilter.html"

    warehouse_concentrates = deep_dict()
    warehouse_concentrates.name = "reports_furnace_area/warehouse_concentrates.html"

    airmachines = deep_dict()
    airmachines.name = "reports_furnace_area/airmachines.html"

    fences_table = deep_dict()
    fences_table.name = "reports_furnace_area/fences_table.html"

    page2_table1 = deep_dict()
    page2_table1.name = "reports_furnace_area/concentration_by_time_table.html"

    page2_table2 = deep_dict()
    page2_table2.name = "reports_furnace_area/places_of_sampling_table.html"

    page2_table3 = deep_dict()
    page2_table3.name = "reports_furnace_area/corrective_actions_table.html"

    page2_table4 = deep_dict()
    page2_table4.name = "reports_furnace_area/self_protection_table.html"

    page2_table5 = deep_dict()
    page2_table5.name = "reports_furnace_area/worth_table.html"

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
