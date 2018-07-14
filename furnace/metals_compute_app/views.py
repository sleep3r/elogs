import pprint

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

from common.all_journals_app.fields_descriptions.fields_info import fields_info_desc
from utils.deep_dict import deep_dict

from common.all_journals_app.models import JournalPage
from common.all_journals_app.services.context_creator import get_common_context



# Create your views here.
from utils.webutils import translate


@login_required
def index(request):
    context = get_common_context(journal_name="metals_compute", request=request)
    context.journal_title = 'Рассчёт металлов'

    main_table = deep_dict()
    main_table.name = 'metals_compute/main_table.html'

    sns_table = deep_dict()
    sns_table.name = "metals_compute/sns_table.html"

    sgok_table = deep_dict()
    sgok_table.name = "metals_compute/sgok_table.html"

    gof_table = deep_dict()
    gof_table.name = "metals_compute/gof_table.html"

    # среднее сожержание за месяц
    avg_month_table = deep_dict()
    avg_month_table.name = "metals_compute/avg_month_table.html"

    contain_zn_table = deep_dict()
    contain_zn_table.name = "metals_compute/contain_zn_table.html"

    cinder_conc_table = deep_dict()
    cinder_conc_table.name = "metals_compute/cinder_conc_table.html"

    concentrat_table = deep_dict()
    concentrat_table.name = "metals_compute/concentrat_table.html"

    context.tables = [
        # avg_month_table,
        contain_zn_table,
        cinder_conc_table,
        concentrat_table,
        main_table,
        sns_table,
        sgok_table,
        gof_table,


                      ]

    context.sgok_table.columns = [
        "ЗГОК, ВМТ",
        "Арт-ий, ВМТ",
        "Усть-ТАЛ, ВМТ",
        "Кара<wbr>гайлы, ВМТ",
        "Верх-Бер, ВМТ",
        "Бело<wbr>усовка, ВМТ",
        "Жез<wbr>кент, ВМТ",
        "Ер Тай, ВМТ",
        "Н.Широ<wbr>кинский, ВМТ",
        "Лесо<wbr>сиб, ВМТ",
        "Алтын-Топкан, ВМТ",
        "итого ВМТ",
        "ИТОГО СМТ",
        "выданно огарка, ВМТ",
        "потери, ВМТ",
        "огарка переданно, ВМТ",
        "ЦЕХ, ВМТ",
        "Лента, ВМТ",
        "потеря бункеров ОВЦО, ВМТ",
        "лента итого, ВМТ",
        "откло<wbr>нение"
    ]

    context.sgok_table.fields = fields_info_desc.metals_compute.sgok_table.keys()
    context.gof_table.fields = fields_info_desc.metals_compute.gof_table.keys()
    context.avg_month_table.fields = fields_info_desc.metals_compute.avg_month_table.keys()

    template = loader.get_template('common.html')
    return HttpResponse(template.render(context, request))
