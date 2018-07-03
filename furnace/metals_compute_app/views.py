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

    context.tables = [
                       main_table,
                       sns_table,
                       sgok_table,
                       gof_table
                      ]

    context.sgok_table.columns = ["ЗГОК",
"Арт-ий",
"Усть-ТАЛ",
"Кара<wbr>гайлы",
"Верх-Бер",
"Бело<wbr>усовка",
"Жез<wbr>кент",
"Ер Тай",
"Н.Широ<wbr>кинский",
"Лесо<wbr>сиб",
"Алтын-Топкан",
"итого ВМТ",
"ИТОГО СМТ",
"выданно огарка",
"потери",
"огарка переданно",
"ЦЕХ",
"Лента",
"потеря бункеров ОВЦО",
"лента итого",
"откло<wbr>нение"]

    context.sgok_table.fields = fields_info_desc.metals_compute.sgok_table.keys()
    context.gof_table.fields = fields_info_desc.metals_compute.gof_table.keys()

    template = loader.get_template('common.html')
    return HttpResponse(template.render(context, request))
