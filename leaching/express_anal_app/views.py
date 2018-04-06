import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect

from django.template import loader
from django.utils import timezone

import datetime
from leaching.express_anal_app import helpers
from leaching.express_anal_app import tables
import pprint

from leaching.express_anal_app.journal_forms import *

from collections import defaultdict

from leaching.express_anal_app.tables import get_free_tanks_table
from utils.webutils import parse, process_json_view
from django.utils.translation import gettext as _
from django.db import transaction

import leaching.express_anal_app.components.agitators


@process_json_view(auth_required=False)
def json_test(request):
    res = get_free_tanks_table(shift=None)
    res['json-test'] = dict(request.GET)
    res['json-post'] = dict(request.POST)
    return res


@process_json_view(auth_required=False)
def json_densers(request):
    answer = {'post': dict(request.POST)}
    return answer


def get_shift_lazy(date, order, plant):
    try:
        shift = Shift.objects.get(date=date, order=order, plant=plant)
    except:
        shift = Shift(date=date, order=order, plant=plant)
        shift.save()

    return shift


@login_required
def index(request):
    context = {
        'hello_list': ['World', 'Darling', 'Inframine', 'Goodbye'],
        'tile_counts': {'total': '31337'},
        'system_messages': [
            {'title': _("Температура кипящего слоя превысила критический показатель"), 'time': "12:33"},
            {'title': _("Всё хорошо"), 'time': "10:33"},
            {'title': _("Надо пошурудить в печи"), 'time': "08:00"}
        ],
        'user_name': str(request.user.employee),
        'notifications': [{
            'type': 'asd',
            'message': "Здорова, как делишки?",
            'id': -1
        }, {
            'type': 'asd',
            'message': "Здорова, как делишки? Здорова, как делишки? Здорова, как делишки? Здорова, как делишки? Здорова, как делишки?",
            'id': -2
        }, {
            'type': 'asd',
            'message': "Здорова, как делишки?",
            'id': -3
        }]
    }

    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))


@process_json_view(auth_required=False)
def notifications_read(request):
    for notification_id in request.POST.getlist('ids[]'):
        None
    return {}

@login_required
def leaching_jurnal(request):
    rows = DenserAnal.objects.all()

    if 'shift' in request.GET:
        shiftId = request.GET['shift']
        results = Shift.objects.filter(id=shiftId)
        if len(results) == 0:
            shift = Shift.objects.all()[0]
        else:
            shift = results[0]

    else:
        shift = Shift.objects.all()[0]

    data_cinder = tables.get_cinder_table(shift)
    data_densers = tables.get_densers_table(shift)
    data_bchc = tables.get_leaching_express_anal_table(shift)
    data_znpulp = {'first': tables.get_solutions_table(shift), 'second': tables.get_solutions2_table(shift)}
    data_hydrometal1 = tables.get_hydrometal1_table(shift)
    data_hydrometal_extra = tables.get_cinder_gran_table(shift)
    data_agitators = tables.get_agitators_table(shift)

    # sheet 2
    data_baki_ready = tables.get_ready_product_table(shift)
    data_neutral = tables.get_neutral_solution_table(shift)
    data_empty_containers = tables.get_free_tanks_table(shift)
    data_neutral_densers = tables.get_neutral_densers_table(shift)
    data_security = tables.get_self_security_table(shift)
    data_schieht = tables.get_schieht_table(shift)
    data_electrolysis = tables.get_electrolysis_table(shift)
    data_reagent = tables.get_reagents_table(shift)
    data_info = tables.get_shift_info_table(shift)

    bchc = {
        'title': _('ВСНС'),
        'columns': [_('ВСНС'), _("Ларокс"), _("Очищенный раствор")],
        'level2': [_("Кобальт Co"), _("Сурьма"), _("Медь"), _("Кадмий"), _("Твердое После 1ст"), "pH (BCHC)", _("Железо"), "As",
                   _("Твёрдое "), _("Уд. вес"),
                   _("Кобальт"), _("Сурьма"), _("Кадмий"), _("Твердое"), "pH", _("Кадмий"), _("Кобальт"), _("Сурьма"), _("Медь"), _("Железо"),
                   _("Выход по току"), _("Уд. вес"), _("Норма"), _("Факт"), _("Несоответствие"), _("Коррекция"), _("Мастер")],
        'data': data_bchc,
        'dump': pprint.pformat(data_bchc, indent=2)
    }

    densers = {
        'title': _('Сгустители'),
        'columns': ['10', "11", "12"],
        'data': data_densers,
        'dump': pprint.pformat(data_densers, indent=4)
    }

    znpulp = {
        'title': _('Пульпа'),
        'columns': ['10', "11", "12"],
        'data': data_znpulp,
        'dump': pprint.pformat(data_znpulp, indent=4)
    }

    apparat = {
        'title': _('Аппаратчик - гидрометаллург'),
        'data': {'main': data_hydrometal1, 'extra': data_hydrometal_extra},
        'dump': pprint.pformat(data_hydrometal1, indent=4)
    }

    agitators = {
        'title': _('Аппаратчик - гидрометаллург'),
        'data': data_agitators,
        'dump': pprint.pformat(data_agitators, indent=4)
    }

    baki = {
        'title': _('Баки готовой продукции'),
        'columns': [_("№ Бака "), _("Кадмий"), _("Медь"), _("Кобальт"), _("Сурьма"), _("Железо"), _("В:T"), _("Уд. вес"), _("Норма"), _("Факт"),
                    _("Коррекция"), _("Мастер")],
        'data': data_baki_ready,
        'dump': pprint.pformat(data_baki_ready)
    }

    neutral = {
        'title': '',
        'columns': {"1": _("Наличие<br>нейтр. р-ра"),
                    "2": _("Уч. выщел. N1<br>бак 3,4,5,4А"),
                    "3": _("Бак") + "3",
                    "4": _("Бак") + "4",
                    "5": _("Итого"),
                    "6": _("Бак III<br/>серии"),
                    "7": _("Бак") + "5",
                    "8": _("Бак") + "6"},
        'data': data_neutral,
        'dump': pprint.pformat(data_neutral)
    }

    electrolysis = {
        'title': _('Нагрузки'),
        'columns': ["", _("I серия"), _("II серия"), _("III серия"), _("IV серия")],
        'rowCaptions': [_("Нагрузки"), _("Показания счётчика"), _("Бункеа ЦВЦО"), _("Силоса ОЦ"), _("Бункера ОЦ")],
        'data': data_electrolysis,
        'dump': pprint.pformat(data_electrolysis)
    }

    empty_containers = {
        'title': _('Наличие свободных ёмкостей'),
        'data': data_empty_containers,
        'dump': pprint.pformat(data_empty_containers)
    }

    neutral_densers = {
        'title': _('Нейтральные сгустители'),
        'data': data_neutral_densers,
        'dump': pprint.pformat(data_neutral_densers)
    }

    security = {
        'title': _('Самоохрана'),
        'data': data_security,
        'dump': pprint.pformat(data_security)
    }

    probnik = {
        'title': _('Пробник №2'),
        'columns': [_("Время"), "Cd", "Cu"],
        'rows': [
            {
                'values': ['', '']
            },
            {
                'values': ['', '']
            },
            {
                'values': ['', '']
            },
            {
                'values': ['', '']
            },
            {
                'values': ['', '']
            },
            {
                'title': _('ВИУ') + '1'
            },
            {
                'title': _('ВИУ') + '2'
            },
            {
                'title': _('ВИУ') + '3'
            }
        ]
    }

    schiehta = {
        'title': _('Шихта'),
        'data': data_schieht,
        'dump': pprint.pformat(data_schieht)
    }

    reagents = {
        'title': _('Реагенты'),
        'data': data_reagent,
        'dump': pprint.pformat(data_reagent)
    }

    shifts = Shift.objects.all()

    context = {
        'title': _("Журнал учёта"),
        'subtitle': _("Цех выщелачивания"),
        'shift': {'date': shift.date, 'num': shift.order, 'data': shift},
        'form_shift': {
            'title': _('Выбранная смена'),
            'currentId': shift.id,
            'data': shifts,
            'dump': pprint.pformat(shifts),
            'action': '/leaching/ju'
        },
        'cinder': {
            'title': _("Огарок"),
            'data': data_cinder.get('0')
        },
        'bchc': bchc,
        'sgustiteli': densers,
        'znpulp': znpulp,
        'apparat': apparat,
        'agitators': agitators,
        'baki': baki,
        'neutral': neutral,
        'electrolysis': electrolysis,
        'empty_containers': empty_containers,
        'neutral_densers': neutral_densers,
        'security': security,
        'probnik': probnik,
        'schiehta': schiehta,
        'reagents': reagents,
        'user_name': str(request.user.employee),

        'info': {'data': data_info, 'dump': pprint.pformat(data_info)},

        'form_validate': None if 'validate' not in request.GET else {
            'action': '//yandex.ru',
            'name': 'validate',
            'value': ''
        }
    }
    if 'print' in request.GET:
    	template = loader.get_template('journal-print.html')
    else:
    	template = loader.get_template('journal.html')
	
    return HttpResponse(template.render(context, request))


@login_required
def leaching_all_edit(request):
    error_messages = ''
    cleaned_data = ''

    if request.method == 'GET':
        # currentDate = timezone.now().strftime("%m/%d/%Y %H:00:00")
        formReagents = ReagentsForm(initial={
            'shlippe': 0,
            'zn_dust': 0,
            'mg_ore': 0,
            'magnaglobe': 0,
            'fe_shave': 0,
            'state': '',
            'stage': '',
            'fence_state': ''
        })

        formReadyTanks = ReadyProductForm()
        formNeuturalDensers = NeuturalDensersForm()
        formExpresAnalysis = ExpressAnalysisForm()
        formDensers = DenserAnalysisForm()
        formZnPulp = ZnPulpForm()
        formCuPulp = CuPulpForm()
        formFeSolution = FeSolutionForm()
        formInputOutput = jea_stand_forms['ShiftInfo']()

    else:
        print('\n----FORM-----')
        print(request.POST)
        print('\n\n')

        # Пока придётся захардкодить поля денормализованной формы
        model = {
            'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
            'fence_state': request.POST['fence_state'],
            'journal': '20',
            'shift': '1'
        }
        modelSt = {
            'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
            'fence_state': request.POST['fence_state'],
            'journal': '20',
            'shift': '1'
        }

        states = ['issued', 'taken', 'delivered', 'consumption']

        for state in states:
            for field in ['shlippe', 'zn_dust', 'mg_ore', 'magnaglobe', 'fe_shave']:
                model[field] = request.POST['states.' + state + '.' + field]
                model['state'] = state
                model['stage'] = 'total'

            form = ReagentsForm(model)  # Bind data from request.POST into a PostForm
            if form.is_valid():
                form.save()
            else:
                print("Not valid\n\n\n")
                print(form.errors)

        stages = ['1st', '2st', '3st', 'cd']
        for stage in stages:
            modelSt['zn_dust'] = request.POST['stages.zn_dust.' + stage]
            modelSt['state'] = 'none'
            modelSt['stage'] = stage

            form = ReagentsForm(modelSt)  # Bind data from request.POST into a PostForm
            if form.is_valid():
                form.save()
            else:
                print("Not valid\n\n\n")
                print(form.errors)

        return HttpResponseRedirect('/leaching/all/edit')

    journal = Journal.objects.get(name='Журнал экспресс анализов')
    if 'shift' in request.GET:
        shiftId = request.GET['shift']
        try:
            shift = Shift.objects.get(id=shiftId) or None
        except:
            shift = Shift.objects.all()[0]
    else:
        shift = Shift.objects.all()[0]


    shifts = Shift.objects.all()

    data_densers = tables.get_densers_table(shift)

    formShiftInfo = jea_stand_forms['ShiftInfo']()

    context = {
        'title': _("Журнал Экспресс анализа (Заполнение)"),
        'vue': True,
        'subtitle': _("Цех выщелачивания"),
        'form_title': _("Заполнить форму"),
        'form_schiehta': {
            'title': _('Шихта'),
            'name': 'form_schiehta',
            'action': '/save/schiehta',
            'shift': shift.id,
        },
        'form_electrolysis': {
            'title': _('Электролиз'),
            'name': 'form_electrolysis',
            'action': '/save/electrolysis',
            'shift': shift.id,
        },
        'form_cinder': {
            'title': _('Огарок'),
            'name': 'form_cinder',
            'action': '/save/cinder',
            'shift': shift.id,
        },
        'form_veu': {
            'title': _('ВИУ'),
            'name': 'form_veu',
            'action': '/save/veu',
            'shift': shift.id,
        },
        'form_sample2': {
            'title': _('Пробник №2'),
            'name': 'form_sample2',
            'action': '/save/sample2',
            'shift': shift.id,
        },
        'form_self_security': {
            'title': _('Самоохрана'),
            'shift': shift.id,
            'name': 'form_self_security',
            'action': '/save/self/security'
        },
        'form_shift': {
            'title': _('Выбранная смена'),
            'currentId': shift.id,
            'data': shifts,
            'dump': pprint.pformat(shifts),
            'action': '/leaching/all/edit'
        },
        'form_shift_info': {
            'title': _('Принято и откачено'),
            'name': 'form_shift_info',
            'fields': formShiftInfo,
            'dump': pprint.pformat(formShiftInfo),
            'action': '/save/shift/info',
            'shift': shift.id,
        },
        'form_empty_tanks': {
            'title': _('Наличие свободных ёмкостей'),
            'name': 'form_empty_tanks',
            'data': get_free_tanks_table(shift),
            'action': '/save/empty/tanks',
            'shift': shift.id,
        },
        'form_reagents': {
            'title': _('Реагенты'),
            'fields': formReagents,
            'name': "form_reagents",
            'action': '',
            'dump': pprint.pformat(formReagents.fields),
            'shift': shift.id,
        },
        'form_ready_tanks': {
            'title': _('Баки готовой продукции'),
            'columns': [_("№ Бака"), _("Кадмий"), _("Медь"), _("Кобальт"), _("Сурьма"), _("Железо"), _("В:T"), _("Уд. вес"), _("Норма"), _("Факт"),
                        _("Коррекция"), _("Мастер")],
            'fields': formReadyTanks,
            'tanks': ['3', '4', '5'],
            'name': 'form_ready_tanks',
            'action': '/save/tanks',
            'shift': shift.id,
        },
        'form_neutural_solution': {
            'title':_('Нейтральный раствор'),
            'name': 'form_neutural_solution',
            'columns': {
                    "1": _("Наличие<br>нейтр. р-ра"),
                    "2": _("Уч. выщел. N1<br>бак 3,4,5,4А"),
                    "3": _("Бак 3"),
                    "4": _("Бак 4"),
                    "5": _("Итого"),
                    "6": _("Бак III<br/>серии"),
                    "7": _("Бак 5"),
                    "8": _("Бак 6")
            },
            'action': '/save/neutural/solution',
            'shift': shift.id,
        },
        'form_densers_neutural': {
            'title': _('Нейтральные сгустители'),
            'name': 'form_densers_neutural',
            'action': '/save/densers/neutural',
            'fields': formNeuturalDensers,
            'densers': ['1', '2', '3', '4', '5', '6', '7', '8', '13'],
            'shift': shift.id,
        },
        'form_express_analysis': {
            'title': _('Экспресс анализ'),
            'name': 'form_express_analysis',
            'action': '/save/express/analysis',
            'fields': formExpresAnalysis,
            'times': ['8', '10', '12', '14', '16', '18', '20'],
            'columns': [_("Кобальт") + " Co", _("Сурьма"), _("Медь"), _("Кадмий"), _("Твердое После 1ст"), "pH (BCHC)", _("Железо"), "As",
                        _("Твёрдое "), _("Уд. вес"),
                        _("Кобальт"), _("Сурьма"), _("Кадмий"), _("Твердое"), "pH", _("Кадмий"), _("Кобальт"), _("Сурьма"), _("Медь"), _("Железо"),
                        _("Выход по току"), _("Уд. вес"), _("Норма"), _("Факт"), _("Несоответствие"), _("Коррекция")],
            'shift': shift.id,
        },
        'form_densers': {
            'name': 'form_densers',
            'title': _('Сгустители'),
            'columns': ['10', "11", "12"],
            'action': '/save/densers',
            'fields': formDensers,
            'previous': data_densers,
            'dump': pprint.pformat(data_densers),
            'shift': shift.id,
        },
        'form_pulps': {
            'title': _('Пульпы'),
            'name': 'form_pulps',
            'action': '/save/pulps',
            'zn': formZnPulp,
            'cu': formCuPulp,
            'fe': formFeSolution,
            'shift': shift.id,
        },
        'form_hydrometal': {
            'title': _('Аппаратчик - Гидрометаллург'),
            'name': 'form_hydrometal',
            'action': '/save/hydrometal',
            'shift': shift.id,

        },
        'form_agitators': {
            'title': _('Агитаторы очистки'),
            'name': 'form_agitators',
            'action': '/save/agitators',
            'shift': shift.id,
        },
        'journal': journal,
        'shift': shift,
        'error_messages': error_messages,
        'data': cleaned_data
    }

    template = loader.get_template('edit.html')
    return HttpResponse(template.render(context, request))


@login_required
def leaching_save_tanks(request):

    journal = Journal.objects.all()[0]
    if 'shift_id' in request.POST:
        shift = Shift.objects.filter(id=request.POST['shift_id'])[0]
    else:
        shift = Shift.objects.all()[0]

    tanks = ['3', '4', '5']
    fields = ['cd', 'cu', 'co', 'sb', 'fe', 'vt', 'density', 'norm', 'fact', 'correction']

    for num in tanks:
        model = {
            'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
            'journal': journal.id,
            'shift': shift.id
        }
        model['num'] = num
        model['verified'] = '1'
        for field in fields:
            model[field] = request.POST['row' + num + '.' + field]

        form = ReadyProductForm(model)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)

    return HttpResponseRedirect('/leaching/all/edit')


@login_required
def leaching_save_neutural_densers(request):
    journal = Journal.objects.all()[0]
    if 'shift_id' in request.POST:
        shift = Shift.objects.filter(id=request.POST['shift_id'])[0]
    else:
        shift = Shift.objects.all()[0]
    densers = ['1', '2', '3', '4', '5', '6', '7', '8', '13']
    fields = [
        'sediment',
        'liq_sol1',
        'liq_sol2'
    ]

    for num in densers:
        model = {
            'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
            'journal': journal.id,
            'shift': shift.id
        }
        model['num'] = num
        for field in fields:
            model[field] = request.POST[field + '_' + num]

        form = NeuturalDensersForm(model)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)

    return HttpResponseRedirect('/leaching/all/edit')


@login_required
def leaching_save_pulps(request):

    journal = Journal.objects.all()[0]
    if 'shift_id' in request.POST:
        shift = Shift.objects.filter(id=request.POST['shift_id'])[0]
    else:
        shift = Shift.objects.all()[0]
    formsCodes = ['zn_pulp', 'cu_pulp', 'fe_sol']
    fields = [
        'liq_sol',
        'ph',
        't0',
        'before',
        'after',
        'solid',
        'h2so4',
        'sb',
        'cu',
        'fe',
        'density',
        'arsenic',
        'cl',
    ]

    for formCode in formsCodes:
        model = {
            'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
            'journal': journal.id,
            'shift': shift.id
        }
        for field in fields:
            postIndex = formCode + '.' + field
            if postIndex in request.POST:
                model[field] = request.POST[postIndex]

        if formCode == 'zn_pulp':
            form = ZnPulpForm(model)
        elif formCode == 'cu_pulp':
            form = CuPulpForm(model)
        elif formCode == 'fe_sol':
            form = FeSolutionForm(model)

        if form.is_valid():
            form.save()
        else:
            print(form.errors)

    return HttpResponseRedirect('leaching/all/edit')


@login_required
def leaching_save_hydrometal(request):

    journal = Journal.objects.all()[0]
    if 'shift_id' in request.POST:
        shift = Shift.objects.filter(id=request.POST['shift_id'])[0]
    else:
        shift = Shift.objects.all()[0]
    employee = Employee.objects.all()[0]
    manns = ['1', '4']
    fields = [
        'ph',
        'acid',
        'fe2',
        'fe_total',
        'cu',
        'sb',
        'sediment',
    ]

    for mannNum in manns:
        model = {
            'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
            'journal': journal.id,
            'shift': shift.id,
            'employee': employee.id
        }
        model['mann_num'] = mannNum
        for field in fields:
            index = 'mann' + mannNum + '.' + field
            if index in request.POST:
                model[field] = request.POST[index]

        form = HydrometalForm(model)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)

    return HttpResponseRedirect('leaching/all/edit')


@login_required
def leaching_save_express_analysis(request):

    journal = Journal.objects.all()[0]

    if 'shift_id' in request.POST:
        shift = Shift.objects.filter(id=request.POST['shift_id'])[0]
    else:
        shift = Shift.objects.all()[0]

    times = ['8', '10', '12', '14', '16', '18', '20']
    fields = [
        'co',
        'sb',
        'cu',
        'cu_st1',
        'cd',
        'solid_st1',
        'ph',
        'fe',
        'arsenic',
        'solid',
        'current',
        'density'
    ]

    prod_fields = ['norm', 'fact', 'error', 'correction']

    points = ['lshs','larox', 'purified', 'prod_correction']

    for num in times:
        model = {
            'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
            'journal': journal.id,
            'shift': shift.id

        }
        dt = datetime.datetime.now()
        model['time'] = dt.replace(hour=int(num), minute=0, second=0, microsecond=0)
        for point in points:
            model['point'] = point
            for field in fields:
                postIndex = 'row.' + point + '.' + field + '_' + num
                if postIndex in request.POST:
                    value = request.POST[postIndex]
                    model[field] = value

            # form = ExpressAnalysisForm(model)
            form = form = jea_stand_forms['LeachingExpressAnal'](model)
            if form.is_valid():
                form.save()
            else:
                print(form.errors)

        prod_model = {
            'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
            'journal': journal.id,
            'shift': shift.id,
            'time': model['time']
        }
        for pf in prod_fields:
            post_index = 'row.prod_correction.' + pf + '_' + num
            if post_index in request.POST:
                prod_model[pf] = request.POST[post_index]

        form = jea_stand_forms['ProductionError'](prod_model)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)


    return HttpResponseRedirect('/leaching/all/edit')


@login_required
def leaching_save_densers(request):
    journal = Journal.objects.all()[0]
    if 'shift_id' in request.POST:
        shift = Shift.objects.filter(id=request.POST['shift_id'])[0]
    else:
        shift = Shift.objects.all()[0]

    densers = ['10', '11', '12']
    sinks = ['hs', 'ls']
    fields = [
        'ph',
        'cu',
        'fe',
        'liq_sol',
    ]

    for denser in densers:

        for sink in sinks:
            model = {
                'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
                'journal': journal.id,
                'shift': shift.id
            }

            model['point'] = denser
            model['sink'] = sink
            # dt = parse('001.01.2018 08:00:00')
            hour = int(request.POST['select_time'])
            dt = datetime.datetime.now()
            model['time'] = dt.replace(hour=hour, minute=0, second=0, microsecond=0)

            for field in fields:
                postIndex = 'denser_' + denser + '.' + sink + '.' + field
                if postIndex in request.POST:
                    model[field] = request.POST[postIndex]

            # form = DenserAnalysisForm(model)
            form = jea_stand_forms['DenserAnalysis'](model)
            if form.is_valid():
                form.save()
            else:
                print(form.errors)

    return HttpResponseRedirect('/leaching/all/edit')


@process_json_view(auth_required=False)
def leaching_save_densers_json(request):
    journal = Journal.objects.all()[0]

    if 'shift_id' in request.POST:
        shift = Shift.objects.filter(id=request.POST['shift_id'])[0]
    else:
        shift = Shift.objects.all()[0]

    densers = ['10', '11', '12']
    sinks = ['hs', 'ls']
    fields = [
        'ph',
        'cu',
        'fe',
        'liq_sol',
    ]

    form_errors = ''

    for denser in densers:
        for sink in sinks:
            model = {
                'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
                'journal': journal.id,
                'shift': shift.id
            }

            model['point'] = denser
            model['sink'] = sink
            hour = int(request.POST['select_time'])
            dt = datetime.datetime.now()
            model['time'] = dt.replace(hour=hour, minute=0, second=0, microsecond=0)

            for field in fields:
                postIndex = 'denser_' + denser + '.' + sink + '.' + field
                if postIndex in request.POST:
                    model[field] = request.POST[postIndex]

            form = jea_stand_forms['DenserAnal'](model)
            if form.is_valid():
                form.save()
            else:
                form_errors = form.errors
                print(form.errors)

    return {
          'result': 'ok',
          'items': tables.get_densers_table(shift),
          'post': dict(request.POST),
          'form_errors': form_errors
    }


@login_required
def leaching_save_shift_info(request):
    print('\n----FORM-----')
    print(request.POST)
    print('\n\n')
    journal = Journal.objects.all()[0]
    if 'shift_id' in request.POST:
        shift = Shift.objects.filter(id=request.POST['shift_id'])[0]
    else:
        shift = Shift.objects.all()[0]

    model = {
        'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
        'journal': journal.id,
        'shift': shift.id,
        'time': datetime.datetime.now(),
        'this_master': request.POST['this_master'],
        'next_master': request.POST['next_master']
    }

    fields = [
        'out_sol_t',
        'out_sol_c',
        'out_pulp_cvck',
        'out_cu_kek',
        'out_cd_sponge',
        'out_electr',
        'out_ruch_cd',
        'out_neutr',
        'out_cu_pulp',
        'in_filtrate_ls',
        'in_filtrate_dens',
        'in_fe',
        'in_fe_hi',
        'in_poor_cd',
    ]

    for field in fields:
        index = 'shift.data.' + field
        if index in request.POST:
            model[field] = request.POST[index]


    form = jea_stand_forms['ShiftInfo'](model)
    if form.is_valid():
        form.save()
    else:
        print(form.errors)


    return HttpResponseRedirect('/leaching/all/edit')


@login_required
def leaching_save_empty_tanks(request):
    print('\n----FORM-----')
    print(request.POST)
    print('\n\n')
    journal = Journal.objects.all()[0]
    if 'shift_id' in request.POST:
        shift = Shift.objects.filter(id=request.POST['shift_id'])[0]
    else:
        shift = Shift.objects.all()[0]

    fields = [
        'str_num',
        'tank_name',
        'prev_measure',
        'cur_measure',
        'deviation',
    ]

    rows = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    for num in rows:
        model = {
            'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
            'journal': journal.id,
            'shift': shift.id,
            'time': datetime.datetime.now(),
        }
        model['str_num'] = str(num)
        for field in fields:
            index = field + '__' + str(num)
            if index in request.POST:
                model[field] = request.POST[index]

        form = jea_stand_forms['FreeTank'](model)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)

    return HttpResponseRedirect('/leaching/all/edit')


@login_required
def leaching_save_neutural_solution(request):
    print('\n----FORM-----')
    print(request.POST)
    print('\n\n')
    journal = Journal.objects.all()[0]
    if 'shift_id' in request.POST:
        shift = Shift.objects.filter(id=request.POST['shift_id'])[0]
    else:
        shift = Shift.objects.all()[0]

    tanks = ['1', '2', '2_2', '3', '4', '5', '6', '7', '8']

    for num in tanks:
        model = {
            'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
            'journal': journal.id,
            'shift': shift.id,
            'time': datetime.datetime.now()
        }
        model['str_num'] = num
        model['tank_name'] = str(request.POST['tank_name_'+num]).replace('<br/>', ' ').strip()
        index_post = 'tank_' + num
        model['value'] = ' '
        print(index_post)

        if index_post in request.POST:
            model['value'] = request.POST[index_post]

        if len(model['value']) == 0:
            model['value'] = '0'

        form = jea_stand_forms['NeutralSolution'](model)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)


    return HttpResponseRedirect('/leaching/all/edit')


@login_required
def leaching_save_schiehta(request):
    print('\n----FORM-----')
    print(request.POST)
    print('\n\n')
    journal = Journal.objects.all()[0]
    shift = Shift.objects.all()[0]

    nums = ['1', '2', '3', '4']
    dt = datetime.datetime.now()
    current_time = dt.replace(minute=0, second=0, microsecond=0)

    for num in nums:
        model = {
            'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
            'journal': journal.id,
            'shift': shift.id,
            'time': current_time,
            'num': num
        }

        model['name'] = request.POST['name_' + num]
        model['value'] = request.POST['value_' + num]


        form = jea_stand_forms['Schieht'](model)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)

    return HttpResponseRedirect('/leaching/all/edit')


@login_required
def leaching_save_electrolysis(request):
    print('\n----FORM-----')
    print(request.POST)
    print('\n\n')
    journal = Journal.objects.all()[0]

    if 'shift_id' in request.POST:
        shift = Shift.objects.filter(id=request.POST['shift_id'])[0]
    else:
        shift = Shift.objects.all()[0]

    dt = datetime.datetime.now()
    current_time = dt.replace(minute=0, second=0, microsecond=0)

    series = ['1', '2', '3', '4']

    fields = [
        'series',
        'loads1',
        'loads2',
        'time1',
        'time2',
        'counter',
        'bunkers_weltz',
        'silos_furnace',
        'bunkers_furnace',
        'comment',
    ]
    for seriea in series:
        model = {
            'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
            'journal': journal.id,
            'shift': shift.id,
            'time': current_time,
        }
        model['series'] = seriea
        model['comment'] = request.POST['comment']
        for field in fields:
            post_index = field + '_' + seriea
            if post_index in request.POST:
                model[field] = request.POST[post_index]


        form = jea_stand_forms['Electrolysis'](model)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)

    return HttpResponseRedirect('/leaching/all/edit')


@login_required
def leaching_save_cinder(request):
    print('\n----FORM-----')
    print(request.POST)
    print('\n\n')

    journal = Journal.objects.all()[0]
    if 'shift_id' in request.POST:
        shift = Shift.objects.filter(id=request.POST['shift_id'])[0]
    else:
        shift = Shift.objects.all()[0]
    dt = datetime.datetime.now()
    current_time = dt.replace(minute=0, second=0, microsecond=0)
    model = {
        'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
        'journal': journal.id,
        'shift': shift.id,
        'time': current_time,
    }

    model['col_num'] = 1
    model['shift_total'] = request.POST['shift_total']
    model['day_total'] = request.POST['day_total']
    model['in_process'] = request.POST['in_process']

    form = jea_stand_forms['Cinder'](model)

    if form.is_valid():
        form.save()
    else:
        print(form.errors)

    return HttpResponseRedirect('/leaching/all/edit')


@login_required
def leaching_save_vue(request):
    print('\n----FORM-----')
    print(request.POST)
    print('\n\n')
    journal = Journal.objects.all()[0]
    if 'shift_id' in request.POST:
        shift = Shift.objects.filter(id=request.POST['shift_id'])[0]
    else:
        shift = Shift.objects.all()[0]
    dt = datetime.datetime.now()
    current_time = dt.replace(minute=0, second=0, microsecond=0)


    rows = ['1', '2', '3']

    fields = [
        'hot',
        'cold',
        'comment',
    ]
    for num in rows:
        model = {
            'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
            'journal': journal.id,
            'shift': shift.id,
            'time': current_time,
        }
        model['num'] = num
        for field in fields:
            post_index = 'veu_' + field + '_' + num
            if post_index in request.POST:
                model[field] = request.POST[post_index]

        form = jea_stand_forms['VEU'](model)

        if form.is_valid():
            form.save()
        else:
            print(form.errors)

    return HttpResponseRedirect('/leaching/all/edit')


@login_required
def leaching_save_sample2(request):
    print('\n----FORM-----')
    print(request.POST)
    print('\n\n')
    journal = Journal.objects.all()[0]
    if 'shift_id' in request.POST:
        shift = Shift.objects.filter(id=request.POST['shift_id'])[0]
    else:
        shift = Shift.objects.all()[0]

    rows = ['1', '2', '3', '4', '5', '6']
    fields = [
        #'time',
        'cd',
        'cu'
    ]

    dt = datetime.datetime.now()

    for num in rows:
        current_time = dt.replace(hour=int(num), minute=0, second=0, microsecond=0)
        model = {
            'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
            'journal': journal.id,
            'shift': shift.id,
            'time': current_time,
        }
        for field in fields:
            post_index = field + '_' + num
            if post_index in request.POST:
                model[field] = request.POST[post_index]

        form = jea_stand_forms['Sample2'](model)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)

    return HttpResponseRedirect('/leaching/all/edit?shift=' + str(shift.id))


@login_required
def leaching_save_self_security(request):
    journal = Journal.objects.all()[0]
    if 'shift_id' in request.POST:
        shift = Shift.objects.filter(id=request.POST['shift_id'])[0]
    else:
        shift = Shift.objects.all()[0]

    dt = datetime.datetime.now()

    rows = ['1', '2', '3']
    fields = [
        'note',
        'bignote'
    ]

    for num in rows:
        hour_index = 'hour_'+num
        if hour_index in request.POST:
            hour = request.POST[hour_index]
        else:
            hour = '1'

        current_time = dt.replace(hour=int(hour), minute=0, second=0, microsecond=0)
        model = {
            'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
            'journal': journal.id,
            'shift': shift.id,
            'time': current_time,
        }

        for field in fields:
            post_index = field + '_' + num
            if post_index in request.POST:
                model[field] = request.POST[post_index]
        model['bignote'] = request.POST['bignote_1']

        form = jea_stand_forms['SelfSecurity'](model)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)

    return HttpResponseRedirect('/leaching/all/edit?shift='+str(shift.id))


@process_json_view(auth_required=False)
def leaching_save_express_analysis_json(request):
    journal = Journal.objects.all()[0]
    if 'shift_id' in request.POST:
        shift = Shift.objects.filter(id=request.POST['shift_id'])[0]
    else:
        shift = Shift.objects.all()[0]

    times = ['8', '10', '12', '14', '16', '18', '20']
    fields = [
        'co',
        'sb',
        'cu',
        'cu_st1',
        'cd',
        'solid_st1',
        'ph',
        'fe',
        'arsenic',
        'solid',
        'current',
        'density'
    ]
    prod_fields = ['norm', 'fact', 'error', 'correction']
    points = ['lshs', 'larox', 'purified', 'prod_correction']
    form_errors = []

    for num in times:
        checkRow = 'time_' + num
        if checkRow in request.POST:
            model = {
                'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
                'journal': journal.id,
                'shift': shift.id

            }
            dt = datetime.datetime.now()
            model['time'] = dt.replace(hour=int(num), minute=0, second=0, microsecond=0)


            for point in points:
                model['point'] = point
                for field in fields:
                    postIndex = 'row.' + point + '.' + field + '_' + num
                    if postIndex in request.POST:
                        value = request.POST[postIndex]
                        model[field] = value
                    else:
                        model[field] = 0



                formE = jea_stand_forms['LeachingExpressAnal'](model)

                if formE.is_valid():
                    formE.save()
                else:
                    form_errors = formE.errors
                    print(formE.errors)

            prod_model = {
                'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
                'journal': journal.id,
                'shift': shift.id,
                'time': model['time']
            }


            for pf in prod_fields:
                post_index = 'row.prod_correction.' + pf + '_' + num
                if post_index in request.POST:
                    prod_model[pf] = request.POST[post_index]
                else:
                    prod_model[pf] = 0

            form = jea_stand_forms['ProductionError'](prod_model)
            if form.is_valid():
                form.save()
            else:
                form_errors = form.errors
                print(form.errors)

    return {
        'result': 'ok',
        'items': tables.get_leaching_express_anal_table(shift),
        'post': dict(request.POST),
        'form_errors': form_errors
    }


@process_json_view(auth_required=False)
def leaching_save_self_security_json(request):

    journal = Journal.objects.all()[0]
    if 'shift_id' in request.POST:
        shift = Shift.objects.filter(id=request.POST['shift_id'])[0]
    else:
        shift = Shift.objects.all()[0]

    dt = datetime.datetime.now()

    rows = ['1', '2', '3']
    fields = [
        'note',
        'bignote'
    ]

    for num in rows:
        hour_index = 'hour_'+num
        if hour_index in request.POST:
            hour = request.POST[hour_index]
        else:
            hour = '1'

        current_time = dt.replace(hour=int(hour), minute=0, second=0, microsecond=0)
        model = {
            'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
            'journal': journal.id,
            'shift': shift.id,
            'time': current_time,
        }

        for field in fields:
            post_index = field + '_' + num
            if post_index in request.POST:
                model[field] = request.POST[post_index]
        model['bignote'] = request.POST['bignote_1']

        form = jea_stand_forms['SelfSecurity'](model)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)

    return {
            'result': 'ok',
            'items': tables.get_self_security_table(shift),
            'post': dict(request.POST)
    }


@process_json_view(auth_required=False)
def leaching_api_express_analysis(request):

    if 'shift_id' in request.GET:
        shift = Shift.objects.filter(id=request.GET['shift_id'])[0]
    else:
        shift = Shift.objects.all()[0]

    if 'hour' in request.GET:
        hour = request.GET['hour']
        items = tables.get_leaching_express_anal_table(shift, hour)
    else:
        items = tables.get_leaching_express_anal_table(shift)

    return {
        'result': 'ok',
        'items': items
    }

@process_json_view(auth_required=False)
def leaching_api_densers(request):
    if 'shift_id' in request.GET:
        shift = Shift.objects.filter(id=request.GET['shift_id'])[0]
    else:
        shift = Shift.objects.all()[0]

    if 'hour' in request.GET:
        hour = request.GET['hour']
        items = tables.get_densers_table(shift, hour)
    else:
        items = tables.get_densers_table(shift)
    return {
        'result': 'ok',
        'items': items,
        'count': len(items)
    }

@process_json_view(auth_required=False)
def leaching_api_hydrometal(request):
    if 'shift_id' in request.GET:
        shift = Shift.objects.filter(id=request.GET['shift_id'])[0]
    else:
        shift = Shift.objects.all()[0]

    items = tables.get_hydrometal1_table(shift)

    return {
        'result': 'ok',
        'items': items,
        'count': len(items),
        'extra': tables.get_cinder_gran_table(shift)
    }

@process_json_view(auth_required=False)
def leaching_save_hydrometal_json(request):
    journal = Journal.objects.all()[0]
    if 'shift_id' in request.POST:
        shift = Shift.objects.filter(id=request.POST['shift_id'])[0]
    else:
        shift = Shift.objects.all()[0]
    employee = Employee.objects.all()[0]
    manns = ['1', '4']
    fields = [
        'ph',
        'acid',
        'fe2',
        'fe_total',
        'cu',
        'sb',
        'sediment',
    ]

    for mannNum in manns:
        model = {
            'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
            'journal': journal.id,
            'shift': shift.id,
            'employee': employee.id
        }
        model['mann_num'] = mannNum
        for field in fields:
            index = 'mann' + mannNum + '.' + field
            if index in request.POST:
                model[field] = request.POST[index]

        form = HydrometalForm(model)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)

    return {
        'result': 'ok',
        'items': tables.get_hydrometal1_table(shift),
        'extra': tables.get_cinder_gran_table(shift)
    }


@process_json_view(auth_required=False)
def leaching_update_hydrometal(request):
    journal = Journal.objects.all()[0]
    data = json.loads(request.POST['item'])

    print(data['shift_id'])
    print(data['extra'])

    if 'shift_id' in data:
        shift = Shift.objects.get(id=data['shift_id'])
    else:
        shift = Shift.objects.all()[0]
    employee = Employee.objects.all()[0]

    fields = [
        'ph',
        'acid',
        'fe2',
        'fe_total',
        'cu',
        'sb',
        'sediment',
        'mann_num'
    ]

    extra_id = data['extra']['id']
    extra_fields = [
        'gran',
        'gran_avg',
        'fe_avg',
        'fe_shave'
    ]

    if extra_id is None:
        cinder_model = CinderDensity()
    else:
        cinder_model = CinderDensity.objects.get(pk=extra_id)

    setattr(cinder_model, 'journal', journal)
    setattr(cinder_model, 'shift', shift)
    for field in extra_fields:
        if field in data['extra']:
            setattr(cinder_model, field, data['extra'][field])

    cinder_model.save()

    manns = ['1','4']
    for man in manns:
        item = data[man]
        if 'id' in item:
            model = HydroMetal.objects.get(pk=item['id'])
        else:
            model = HydroMetal()
            setattr(model, 'mann_num', man)
            setattr(model, 'journal', journal)
            setattr(model, 'shift', shift)
            setattr(model, 'employee', employee)

        for field in fields:
            if field in item:
                setattr(model, field, item[field])
        model.save()

    return {
        'result': 'ok',
    }


@process_json_view(auth_required=False)
def leaching_save_hydrometal_remove(request):
    id = request.GET['id']
    record = HydroMetal.objects.filter(id=id).delete()

    return {
        'action': 'remove',
        'id': id,
        'record': record
    }


@process_json_view(auth_required=False)
def leaching_api_pulps(request):
    if 'shift_id' in request.GET:
        shift = Shift.objects.get(id=request.GET['shift_id'])
    else:
        shift = Shift.objects.all()[0]

    return {
        'result': 'ok',
        'items': tables.get_solutions_table(shift),
        'extra': tables.get_solutions2_table(shift)
    }


@process_json_view(auth_required=False)
def leaching_update_pulps(request):
    journal = Journal.objects.get(name='Журнал экспресс анализов')
    data = json.loads(request.POST['items'])

    if 'shift_id' in data:
        shift = Shift.objects.get(id=data['shift_id'])
    else:
        shift = Shift.objects.all()[0]

    zn_fields = [f.name for f in ZnPulpAnal._meta.get_fields(include_parents=False) if f.name != 'cu_pulp_anal' if f.name != 'fe_solution_anal' if f.name != 'journaltable_ptr']
    cu_fields = [f.name for f in CuPulpAnal._meta.get_fields(include_parents=False) if f.name != 'zn_pulp_anal' if f.name != 'fe_solution_anal' if f.name != 'journaltable_ptr']
    fe_fields = [f.name for f in FeSolutionAnal._meta.get_fields(include_parents=False) if f.name != 'cu_pulp_anal' if f.name != 'zn_pulp_anal' if f.name != 'journaltable_ptr']
    da_fields = [f.name for f in DailyAnalysis._meta.get_fields(include_parents=False) if f.name != 'journaltable_ptr']

    if 'id' in data['zn_pulp']:
        zn_pulp = ZnPulpAnal.objects.get(pk=int(data['zn_pulp']['id']))
    else:
        zn_pulp = ZnPulpAnal()

    if 'id' in data['cu_pulp']:
        cu_pulp = CuPulpAnal.objects.get(pk=int(data['cu_pulp']['id']))
    else:
        cu_pulp = CuPulpAnal()

    if 'id' in data['fe_sol']:
        fe_sol = FeSolutionAnal.objects.get(pk=int(data['fe_sol']['id']))
    else:
        fe_sol = FeSolutionAnal()

    if 'id' in data['extra']:
        day_anal = DailyAnalysis.objects.get(pk=int(data['extra']['id']))
    else:
        day_anal = DailyAnalysis()

    for field in da_fields:
        setattr(day_anal, field, data['extra'][field])
    day_anal.save()

    for field in zn_fields:
        setattr(zn_pulp, field, data['zn_pulp'].get(field) or 0)

    setattr(zn_pulp,'shift', shift)
    zn_pulp.journal = journal
    zn_pulp.cu_pulp_anal = cu_pulp
    zn_pulp.fe_sol_anal = fe_sol
    zn_pulp.save()

    for field in cu_fields:
        setattr(cu_pulp, field, data['cu_pulp'].get(field) or 0)
    setattr(cu_pulp, 'shift', shift)
    cu_pulp.zn_pulp_anal = zn_pulp
    cu_pulp.fe_sol_anal = fe_sol
    cu_pulp.journal = journal
    cu_pulp.save()

    for field in fe_fields:
        setattr(fe_sol, field, data['fe_sol'].get(field) or 0)
    setattr(fe_sol, 'shift', shift)
    fe_sol.zn_pulp_anal = zn_pulp
    fe_sol.cu_pulp_anal = cu_pulp
    fe_sol.save()

    return {
        'result': 'ok',
        'data': data
    }

@process_json_view(auth_required=False)
def leaching_pulps_remove(request):
    combid = request.GET['combid']

    ids = combid.split(';')

    record1 = ZnPulpAnal.objects.filter(id=ids[0]).delete()
    record2 = CuPulpAnal.objects.filter(id=ids[1]).delete()
    record3 = DailyAnalysis.objects.filter(id=ids[2]).delete()

    return {
        'action': 'remove',
        'id': id,
        'record': record1
    }


@process_json_view(auth_required=False)
def leaching_make_shift(request):
    date_time = datetime.datetime.now()
    shift_date = date_time.replace(hour=8, minute=0, second=0, microsecond=0)
    plant = 'leaching'
    shift = get_shift_lazy(shift_date, 1, plant)

    return {
        'result': 'ok',
        'shift': shift
    }


@login_required
def leaching_wizard(request):
    context = {}
    template = loader.get_template('react-table-edit.html')
    return HttpResponse(template.render(context, request))
