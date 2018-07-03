# express_analysis

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from utils.deep_dict import deep_dict
from django.template import loader
from common.all_journals_app.models import JournalPage
from common.all_journals_app.services.context_creator import get_common_context
from django.utils.translation import gettext as _


@login_required
def index(request):
    context = get_common_context(journal_name="leaching_express_analysis", request=request)
    context.journal_title = "Журнал экспресс анализа"

    template = loader.get_template('common.html')

    vsns_table = deep_dict()
    vsns_table.title = "BCHC"
    vsns_table.name = "express_analysis/vsns_table.html"

    appt_hydrometal_table = deep_dict()
    appt_hydrometal_table.title = "Аппаратчик - гидрометаллург"
    appt_hydrometal_table.name = "express_analysis/appt_hydrometal_table.html"

    context.vsns_table.columns = [_("Кобальт Co") + _(', мг/л'), _("Сурьма") + _(', мг/л'), _("Медь") + _(', мг/л'), _("Кадмий"),
               _("Твердое После 1ст") + _(', г/л'), "pH (BCHC)", _("Железо Fe") + _(', мг/л'), "As" + _(', мг/л'),
               _("Твёрдое") + _(', г/л'), _("Уд. вес"),
               _("Кобальт") + _(', мг/л'), _("Сурьма") + _(', мг/л'), _("Кадмий") + _(', мг/л'),
               _("Твердое") + _(', г/л'), "pH", _("Кадмий") + _(', мг/л'), _("Кобальт") + _(', мг/л'),
               _("Сурьма") + _(', мг/л'), _("Медь") + _(', мг/л'), _("Железо") + _(', мг/л'),
               _("Выход по току"), _("Уд. вес"), _("Норма") + _(', мг/л'), _("Факт") + _(', мг/л'),
               _("Несоответствие") + _(', мг/л'), _("Коррекция"), _("Мастер")]



    context.tables = [
        vsns_table,
        appt_hydrometal_table
    ]
    return HttpResponse(template.render(context, request))
