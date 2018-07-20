# express_analysis

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from e_logs.core.utils.deep_dict import deep_dict
from django.template import loader
from e_logs.common.all_journals_app.models import JournalPage
from e_logs.common.all_journals_app.services.context_creator import get_common_context
from django.utils.translation import gettext as _


@login_required
def index(request):
    context = get_common_context(journal_name="leaching_express_analysis", request=request)
    context.journal_title = "Журнал экспресс анализа"

    template = loader.get_template('common.html')

    shift_info_table = deep_dict()
    shift_info_table.name = "express_analysis/shift_info_table.html"

    vsns_table = deep_dict()
    vsns_table.name = "express_analysis/vsns_table.html"

    appt_hydrometal_table = deep_dict()
    appt_hydrometal_table.name = "express_analysis/appt_hydrometal_table.html"

    agitators_table = deep_dict()
    agitators_table.name = "express_analysis/agitators_table.html"

    thickeners_table = deep_dict()
    thickeners_table.name = "express_analysis/thickeners_table.html"

    zinc_pulp_table = deep_dict()
    zinc_pulp_table.name = "express_analysis/zinc_pulp_table.html"

    reagents_table = deep_dict()
    reagents_table.name = "express_analysis/reagents_table.html"

    tanks_availability_table = deep_dict()
    tanks_availability_table.name = "express_analysis/tanks_availability_table.html"
    
    neutral_thickeners_table = deep_dict()
    neutral_thickeners_table.name = "express_analysis/neutral_thickeners_table.html"

    self_protection_table = deep_dict()
    self_protection_table.name = "express_analysis/self_protection_table.html"

    cinder_table = deep_dict()
    cinder_table.name = "express_analysis/cinder_table.html"

    schieht_table = deep_dict()
    schieht_table.name = "express_analysis/schieht_table.html"

    tanks_for_finished_products_table = deep_dict()
    tanks_for_finished_products_table.name = "express_analysis/tanks_for_finished_products_table.html"

    loads_table = deep_dict()
    loads_table.name = "express_analysis/loads_table.html"

    sample_table = deep_dict()
    sample_table.name = "express_analysis/sample_table.html"

    neutral_table = deep_dict()
    neutral_table.name = "express_analysis/neutral_table.html"

    context.tables = [
        appt_hydrometal_table,
        shift_info_table,
        vsns_table,
        thickeners_table,
        zinc_pulp_table,
        agitators_table,
        reagents_table,
        tanks_availability_table,
        neutral_thickeners_table,
        self_protection_table,
        cinder_table,
        schieht_table,
        loads_table,
        sample_table,
        tanks_for_finished_products_table,
        neutral_table,
    ]

    return HttpResponse(template.render(context, request))
