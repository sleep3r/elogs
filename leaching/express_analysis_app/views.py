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

    context.vsns_table.columns = [_("Кобальт Co") + _(', мг/л'), _("Сурьма") + _(', мг/л'), _("Медь") + _(', мг/л'),
                                  _("Кадмий"),
                                  _("Твердое После 1ст") + _(', г/л'), "pH (BCHC)", _("Железо Fe") + _(', мг/л'),
                                  "As" + _(', мг/л'),
                                  _("Твёрдое") + _(', г/л'), _("Уд. вес"),
                                  _("Кобальт") + _(', мг/л'), _("Сурьма") + _(', мг/л'), _("Кадмий") + _(', мг/л'),
                                  _("Твердое") + _(', г/л'), "pH", _("Кадмий") + _(', мг/л'),
                                  _("Кобальт") + _(', мг/л'),
                                  _("Сурьма") + _(', мг/л'), _("Медь") + _(', мг/л'), _("Железо") + _(', мг/л'),
                                  _("Выход по току"), _("Уд. вес"), _("Норма") + _(', мг/л'), _("Факт") + _(', мг/л'),
                                  _("Несоответствие") + _(', мг/л'), _("Коррекция"), _("Мастер")]

    shift_info_table = deep_dict()
    shift_info_table.name = "express_analysis/shift_info_table.html"

    vsns_table = deep_dict()
    vsns_table.title = "BCHC"
    vsns_table.name = "express_analysis/vsns_table.html"

    appt_hydrometal_table = deep_dict()
    appt_hydrometal_table.title = "Аппаратчик - гидрометаллург"
    appt_hydrometal_table.name = "express_analysis/appt_hydrometal_table.html"

    agitators_table = deep_dict()
    agitators_table.title = "Агитаторы очистки"
    agitators_table.name = "express_analysis/agitators_table.html"

    thickeners_table = deep_dict()
    thickeners_table.title = "Сгустители"
    thickeners_table.name = "express_analysis/thickeners_table.html"
    context.thickeners_table.columns = [_("pH"), _("Медь")+ _(', мг/л'), _("Железо")+ _(', мг/л'), _("Ж:Т"), _("pH"), _("Ж:Т")] * 3


    zinc_pulp_table = deep_dict()
    zinc_pulp_table.title = "Цинковая пульпа"
    zinc_pulp_table.name = "express_analysis/zinc_pulp_table.html"

    reagents_table = deep_dict()
    reagents_table.title = "Реагенты"
    reagents_table.name = "express_analysis/reagents_table.html"



    tanks_availability_table = deep_dict()
    tanks_availability_table.title = "Наличие свободных ёмкостей"
    tanks_availability_table.name = "express_analysis/tanks_availability_table.html"
    context.tanks_availability_table.columns = [_("Бак отработ. 1-2 серий"), 
                                                _("Манны") + " №1-9", 
                                                _("Манны") + _(" ВТВ") + " №10-12", 
                                                _("Обор-й сгуститель") + " №9", 
                                                _("Агитатор") + " 22", 
                                                _("Бак нейтр. р-ра") + _(", 1-й цех"),
                                                _("Ман отраб.") + " №2" + _(", 1-й цех"),  
                                                _("Ман отраб.") + " №3" + _(", 1-й цех"),
                                                _("Ман отраб.") + " №9" + _(", 1-й цех"), 
                                                "-", 
                                                _("СМЕННЫЙ БАЛАНС"), 
                                                _("СУТОЧНЫЙ БАЛАНС")]

    context.tanks_availability_table.db_columns = {1:("prev_measurements_waste_tank_1-2seria", "current_measurements_waste_tank_1-2seria", "divergence_waste_tank_1-2seria"),
                                                   2:("prev_measurements_manns_1-9", "current_measurements_manns_1-9", "divergence_manns_1-9"),
                                                   3:("prev_measurements_manns_VTV_10-12", "current_measurements_manns_VTV_10-12", "divergence_manns_VTV_10-12"),
                                                   4:("prev_measurements_thickener-9", "current_measurements_thickener-9", "divergence_thickener-9"),
                                                   5:("prev_measurements_agitator-22", "current_measurements_agitator-22", "divergence_agitator-22"),
                                                   6:("prev_measurements_neutral_tank", "current_measurements_neutral_tank", "divergence_neutral_tank"),
                                                   7:("prev_measurements_waste_mann-2", "current_measurements_waste_mann-2", "divergence_waste_mann-2"),
                                                   8:("prev_measurements_waste_mann-3", "current_measurements_waste_mann-3", "divergence_waste_mann-3"),
                                                   9:("prev_measurements_waste_mann-9", "current_measurements_waste_mann-9", "divergence_waste_mann-9"),
                                                  10:("prev_measurements_-", "current_measurements_-", "divergence_-"),
                                                  11:("prev_measurements_removable_balance", "current_measurements_removable_balance", "divergence_removable_balance"),
                                                  12:("prev_measurements_daily_balance", "current_measurements_daily_balance", "divergence_daily_balance")}


    neutral_thickeners_table = deep_dict()
    neutral_thickeners_table.title = "Нейтральные сгустители"
    neutral_thickeners_table.name = "express_analysis/neutral_thickeners_table.html"


    self_protection_table = deep_dict()
    self_protection_table.title = "Самоохрана"
    self_protection_table.name = "express_analysis/self_protection_table.html"

    cinder_table = deep_dict()
    cinder_table.title = "Огарок"
    cinder_table.name = "express_analysis/cinder_table.html"

    schieht_table = deep_dict()
    schieht_table.title = "Шихта"
    schieht_table.name = "express_analysis/schieht_table.html"


    tanks_for_finished_products_table = deep_dict()
    tanks_for_finished_products_table.title = "Баки готовой продукции"
    tanks_for_finished_products_table.name = "express_analysis/tanks_for_finished_products_table.html"


    loads_table = deep_dict()
    loads_table.title = "Нагрузки"
    loads_table.name = "express_analysis/loads_table.html"

    sample_table = deep_dict()
    sample_table.title = "Пробник"
    sample_table.name = "express_analysis/sample_table.html"

    neutral_table = deep_dict()
    neutral_table.title = "Нейтральный р-р"
    neutral_table.name = "express_analysis/neutral_table.html"

    context.tables = [
        shift_info_table,
        vsns_table,
        appt_hydrometal_table,
        thickeners_table,
        zinc_pulp_table,
        agitators_table,
        reagents_table,
        tanks_availability_table,
        neutral_thickeners_table,
        self_protection_table,
        cinder_table,
        schieht_table,
        reagents_table,
        loads_table,
        sample_table,
        tanks_for_finished_products_table,
        neutral_table,
    ]

    return HttpResponse(template.render(context, request))
