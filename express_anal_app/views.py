import json

from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect

from django.template import loader
from django.utils import timezone

import datetime
from express_anal_app import helpers
from express_anal_app import tables
import pprint

from express_anal_app.journal_forms import *

from collections import defaultdict

from express_anal_app.tables import get_free_tanks_table
from utils.webutils import parse, process_json_view
from django.db import transaction


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


def index(request):
    context = {
        'hello_list': ['World', 'Darling', 'Inframine', 'Goodbye'],
        'tile_counts': {'total': '31337'},
        'system_messages': [
            {'title': "Температура кипящего слоя превысила критический показатель", 'time': "12:33"},
            {'title': "Всё хорошо", 'time': "10:33"},
            {'title': "Надо пошурудить в печи", 'time': "08:00"}
        ]
    }

    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))


def leaching_ju(request):
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
        'title': 'BCHC',
        'columns': ['BCHC', "Ларокс", "Очищенный раствор"],
        'level2': ["Кобальт Co", "Сурьма", "Медь", "Кадмий", "Твердое После 1ст", "pH (BCHC)", "Железо", "As",
                   "Твёрдое ", "Уд. вес",
                   "Кобальт", "Сурьма", "Кадмий", "Твердое", "pH", "Кадмий", "Кобальт", "Сурьма", "Медь", "Железо",
                   "Выход по току", "Уд. вес", "Норма", "Факт", "Несоответствие", "Коррекция", "Мастер"],
        'data': data_bchc,
        'dump': pprint.pformat(data_bchc, indent=2)
    }

    densers = {
        'title': 'Сгустители',
        'columns': ['10', "11", "12"],
        'data': data_densers,
        'dump': pprint.pformat(data_densers, indent=4)
    }

    znpulp = {
        'title': 'Пульпа',
        'columns': ['10', "11", "12"],
        'data': data_znpulp,
        'dump': pprint.pformat(data_znpulp, indent=4)
    }

    apparat = {
        'title': 'Аппаратчик - гидрометаллург',
        'data': {'main': data_hydrometal1, 'extra': data_hydrometal_extra},
        'dump': pprint.pformat(data_hydrometal1, indent=4)
    }

    agitators = {
        'title': 'Аппаратчик - гидрометаллург',
        'data': data_agitators,
        'dump': pprint.pformat(data_agitators, indent=4)
    }

    baki = {
        'title': 'Баки готовой продукции',
        'columns': ["№ Бака ", "Кадмий", "Медь", "Кобальт", "Сурьма", "Железо", "В:T", "Уд. вес", "Норма", "Факт",
                    "Коррекция", "Мастер"],
        'data': data_baki_ready,
        'dump': pprint.pformat(data_baki_ready)
    }

    neutral = {
        'title': '',
        'columns': {"1": "Наличие<br>нейтр. р-ра",
                    "2": "Уч. выщел. N1<br>бак 3,4,5,4А",
                    "3": "Бак 3",
                    "4": "Бак 4",
                    "5": "Итого",
                    "6": "Бак III<br/>серии",
                    "7": "Бак 5",
                    "8": "Бак 6"},
        'data': data_neutral,
        'dump': pprint.pformat(data_neutral)
    }

    electrolysis = {
        'title': 'Нагрузки',
        'columns': ["", "I серия", "II серия", "III серия", "IV серия"],
        'rowCaptions': ["Нагрузки", "Показания счётчика", "Бункеа ЦВЦО", "Силоса ОЦ", "Бункера ОЦ"],
        'data': data_electrolysis,
        'dump': pprint.pformat(data_electrolysis)
    }

    empty_containers = {
        'title': 'Наличие свободных ёмкостей',
        'data': data_empty_containers,
        'dump': pprint.pformat(data_empty_containers)
    }

    neutral_densers = {
        'title': 'Нейтральные сгустители',
        'data': data_neutral_densers,
        'dump': pprint.pformat(data_neutral_densers)
    }

    security = {
        'title': 'Самоохрана',
        'data': data_security,
        'dump': pprint.pformat(data_security)
    }

    probnik = {
        'title': 'Пробник №2',
        'columns': ["Время", "Cd", "Cu"],
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
                'title': 'ВИУ 1'
            },
            {
                'title': 'ВИУ 2'
            },
            {
                'title': 'ВИУ 3'
            }
        ]
    }

    schiehta = {
        'title': 'Шихта',
        'data': data_schieht,
        'dump': pprint.pformat(data_schieht)
    }

    reagents = {
        'title': 'Реагенты',
        'data': data_reagent,
        'dump': pprint.pformat(data_reagent)
    }

    shifts = Shift.objects.all()

    context = {
        'title': "Журнал учёта ",
        'subtitle': "Цех выщелачивания",
        'shift': {'date': shift.date, 'num': shift.order, 'data': shift},
        'form_shift': {
            'title': 'Выбранная смена',
            'currentId': shift.id,
            'data': shifts,
            'dump': pprint.pformat(shifts),
            'action': '/leaching/ju'
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

        'info': {'data': data_info, 'dump': pprint.pformat(data_info)}
    }

    template = loader.get_template('journal.html')
    return HttpResponse(template.render(context, request))


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

    journal = Journal.objects.all()[0]
    if 'shift' in request.GET:
        shiftId = request.GET['shift']
        shift = Shift.objects.filter(id=shiftId)[0]
    else:
        shift = Shift.objects.all()[0]


    shifts = Shift.objects.all()

    data_densers = tables.get_densers_table(shift)

    formShiftInfo = jea_stand_forms['ShiftInfo']()

    context = {
        'title': "Журнал Экспресс анализа (Заполнение)",
        'vue': True,
        'subtitle': "Цех выщелачивания",
        'form_title': "Заполнить форму",
        'form_schiehta': {
            'title': 'Шихта',
            'name': 'form_schiehta',
            'action': '/save/schiehta',
            'shift': shift.id,
        },
        'form_electrolysis': {
            'title': 'Электролиз',
            'name': 'form_electrolysis',
            'action': '/save/electrolysis',
            'shift': shift.id,
        },
        'form_cinder': {
            'title': 'Огарок',
            'name': 'form_cinder',
            'action': '/save/cinder',
            'shift': shift.id,
        },
        'form_veu': {
            'title': 'ВИУ',
            'name': 'form_veu',
            'action': '/save/veu',
            'shift': shift.id,
        },
        'form_sample2': {
            'title': 'Пробник №2',
            'name': 'form_sample2',
            'action': '/save/sample2',
            'shift': shift.id,
        },
        'form_self_security': {
            'title': 'Самоохрана',
            'shift': shift.id,
            'name': 'form_self_security',
            'action': '/save/self/security'
        },
        'form_shift': {
            'title': 'Выбранная смена',
            'currentId': shift.id,
            'data': shifts,
            'dump': pprint.pformat(shifts),
            'action': '/leaching/all/edit'
        },
        'form_shift_info': {
            'title': 'Принято и откачено',
            'fields': formShiftInfo,
            'dump': pprint.pformat(formShiftInfo),
            'action': '/save/shift/info',
            'shift': shift.id,
        },
        'form_empty_tanks': {
            'title': 'Наличие свободных ёмкостей',
            'data': get_free_tanks_table(shift),
            'action': '/save/empty/tanks',
            'shift': shift.id,
        },
        'form_reagents': {
            'title': 'Реагенты',
            'fields': formReagents,
            'name': "form_reagents",
            'action': '',
            'dump': pprint.pformat(formReagents.fields),
            'shift': shift.id,
        },
        'form_ready_tanks': {
            'title': 'Баки готовой продукции',
            'columns': ["№ Бака ", "Кадмий", "Медь", "Кобальт", "Сурьма", "Железо", "В:T", "Уд. вес", "Норма", "Факт",
                        "Коррекция", "Мастер"],
            'fields': formReadyTanks,
            'tanks': ['3', '4', '5'],
            'name': 'form_ready_tanks',
            'action': '/save/tanks',
            'shift': shift.id,
        },
        'form_neutural_solution': {
            'title':'Нейтральный раствор',
            'columns': {
                    "1": "Наличие<br>нейтр. р-ра",
                    "2": "Уч. выщел. N1<br>бак 3,4,5,4А",
                    "3": "Бак 3",
                    "4": "Бак 4",
                    "5": "Итого",
                    "6": "Бак III<br/>серии",
                    "7": "Бак 5",
                    "8": "Бак 6"
            },
            'action': '/save/neutural/solution',
            'shift': shift.id,
        },
        'form_densers_neutural': {
            'title': 'Нейтральные сгустители',
            'name': 'form_densers_neutural',
            'action': '/save/densers/neutural',
            'fields': formNeuturalDensers,
            'densers': ['1', '2', '3', '4', '5', '6', '7', '8', '13'],
            'shift': shift.id,
        },
        'form_express_analysis': {
            'title': 'Экспресс анализ',
            'name': 'form_express_analysis',
            'action': '/save/express/analysis',
            'fields': formExpresAnalysis,
            'times': ['8', '10', '12', '14', '16', '18', '20'],
            'columns': ["Кобальт Co", "Сурьма", "Медь", "Кадмий", "Твердое После 1ст", "pH (BCHC)", "Железо", "As",
                        "Твёрдое ", "Уд. вес",
                        "Кобальт", "Сурьма", "Кадмий", "Твердое", "pH", "Кадмий", "Кобальт", "Сурьма", "Медь", "Железо",
                        "Выход по току", "Уд. вес", "Норма", "Факт", "Несоответствие", "Коррекция"],
            'shift': shift.id,
        },
        'form_densers': {
            'title': 'Сгустители',
            'name': 'form_densers',
            'columns': ['10', "11", "12"],
            'action': '/save/densers',
            'fields': formDensers,
            'previous': data_densers,
            'dump': pprint.pformat(data_densers),
            'shift': shift.id,
        },
        'form_pulps': {
            'title': 'Пульпы',
            'name': 'form_pulps',
            'action': '/save/pulps',
            'zn': formZnPulp,
            'cu': formCuPulp,
            'fe': formFeSolution,
            'shift': shift.id,
        },
        'form_hydrometal': {
            'title': 'Аппаратчик - Гидрометаллург',
            'name': 'form_hydrometal',
            'action': '/save/hydrometal',
            'shift': shift.id,

        },
        'form_agitators': {
            'title': 'Агитаторы очистки',
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


def leaching_save_agitators(request):
    print('\n----FORM-----')
    print(request.POST)
    print('\n\n')
    journal = Journal.objects.all()[0]
    if 'shift_id' in request.POST:
        shift = Shift.objects.filter(id=request.POST['shift_id'])[0]
    else:
        shift = Shift.objects.all()[0]
    employee = Employee.objects.all()[0]
    agitators = ['13', '15', '17', '19']
    states = ['before', 'after']
    rows = ['1', '2', '3']

    fields = [
        'ph',
        'cu',
        'co',
        'cd',
        'h2so4'
    ]
    for num in agitators:
        for state in states:
            for rowNum in rows:
                model = {
                    'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
                    'journal': journal.id,
                    'shift': shift.id,
                    'employee': employee.id,
                    'num': num
                }
                model['before']   = 1 if state == 'before' else 0
                model['comment'] = request.POST['comment']
                for field in fields:
                    index = 'agitator' + num + '.'+ state + '.' + field + '_' + rowNum
                    print(index)
                    if index in request.POST:

                        model[field] = request.POST[index]

                form = AgitatorsForm(model)
                if form.is_valid():
                    form.save()
                else:
                    print(form.errors)

    return HttpResponseRedirect('leaching/all/edit')


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
        'count': len(items)
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
    }


@process_json_view(auth_required=False)
@transaction.atomic
def leaching_update_hydrometal(request):
    journal = Journal.objects.all()[0]
    data = json.loads(request.POST['item'])

    print(data['shift_id'])

    if 'shift_id' in data:
        shift = Shift.objects.get(id=data['shift_id'])
    else:
        shift = Shift.objects.all()[0]
    employee = Employee.objects.all()[0]


    print(data)
    print(data['1'])
    print(data['4'])
    print(shift)

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
        'dump': pprint.pformat(request.POST)
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


def leaching_wizard(request):
    context = {}
    template = loader.get_template('react-table-edit.html')
    return HttpResponse(template.render(context, request))
