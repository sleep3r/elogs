import json

from django.http import HttpResponse
from django.http import HttpResponseRedirect


from django.template import loader
from django.utils import timezone

import datetime
from express_anal_app import helpers
from express_anal_app import tables
import pprint

from express_anal_app.journal_forms import *

from collections import defaultdict
def deep_dict():
    return defaultdict(deep_dict)




def index(request):
    context = {
        'hello_list': ['World', 'Darling', 'Inframine', 'Goodbye'],
        'tile_counts': {'total': '31337'},
        'system_messages': [
            { 'title': "Температура кипящего слоя превысила критический показатель", 'time': "12:33"},
            { 'title': "Всё хорошо",  'time': "10:33"},
            { 'title': "Надо пошурудить в печи",  'time': "08:00"}
        ]
    }

    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))


def leaching_ju(request):

    rows = DenserAnal.objects.all()
    shift = Shift.objects.all()[0]

    helpers.dump(rows)

    data_densers = tables.get_densers_table(shift)
    data_bchc = tables.get_leaching_express_anal_table(shift)
    data_znpulp = {'first': tables.get_solutions_table(shift), 'second':tables.get_solutions2_table(shift)}
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
        'data': data_densers, # helpers.denserData(),
        'dump': pprint.pformat(data_densers, indent=4)
    }

    znpulp = {
        'title': 'Пульпа',
        'columns': ['10', "11", "12"],
        'data': data_znpulp,  # helpers.denserData(),
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
        'columns': ["№ Бака ", "Кадмий", "Медь", "Кобальт", "Сурьма","Железо","В:T","Уд. вес","Норма", "Факт", "Коррекция", "Мастер"],
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
        'title':'Шихта',
        'data': data_schieht,
        'dump': pprint.pformat(data_schieht)
    }

    reagents = {
        'title': 'Реагенты',
        'data': data_reagent,
        'dump': pprint.pformat(data_reagent)
    }

    context = {
        'title': "Журнал учёта ",
        'subtitle': "Цех выщелачивания",
        'shift': {'date': shift.date, 'num': shift.order, 'data': shift},
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

    template = loader.get_template('densers.html')
    return HttpResponse(template.render(context, request))

def electrolysis(request):

    context = {
        'title': "Журнал Экспресс анализа",
        'subtitle': "Цех выщелачивания"
    }

    template = loader.get_template('journal.html')
    return HttpResponse(template.render(context, request))


def leaching_jrk(request):
    context = {
        'title': "Журнал расхода серной кислоты",
        'subtitle': "Цех выщелачивания"
    }
    template = loader.get_template('journal.html')
    return HttpResponse(template.render(context, request))


def electrolysisEdit(request):
    if request.method == 'GET':
        form = PostForm()
    else:
        form = PostForm(request.POST) # Bind data from request.POST into a PostForm
        if form.is_valid():
            dump = form.cleaned_data['ph']
            # created_at = form.cleaned_data['created_at']

    context = {
        'form': form
    }
    template = loader.get_template('react-table-edit.html')
    return HttpResponse(template.render(context, request))


def leaching_jea_edit(request):
    error_messages = ''
    cleaned_data = ''

    if request.method == 'GET':
        currentDate = timezone.now().strftime("%m/%d/%Y %H:00:00")

        form = DenserForm(initial={
            'journal': '1',
            'shift': '1',
            'point': '10',
            'sink': '0',
            'ph':'0.0',
            'cu':'0.0',
            'fe': '0.0',
            'liq_sol': '0.1',
            'time': currentDate})

        form.error_css_class = 'label label-danger'

    else:
        form = DenserForm(request.POST) # Bind data from request.POST into a PostForm

        if form.is_valid():
            form.save()
            #return HttpResponseRedirect(request.path_info)
            return  HttpResponseRedirect('/leaching/ju')
        else:
            error_messages = form.errors
            cleaned_data = form.cleaned_data


    journal = Journal.objects.all()[0]
    shift  = Shift.objects.all()[0]

    context = {
            'title': "Журнал Экспресс анализа (Edit)",
            'subtitle': "Цех выщелачивания",
            'form_title': "Заполнить форму",
            'form': form,
            'journal': journal,
            'shift': shift,
            'error_messages': error_messages,
            'data': cleaned_data
    }

    template = loader.get_template('journal-edit.html')
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

    else:
        print('\n----FORM-----')
        print(request.POST)
        print('\n\n')


        # Пока придётся захардкодить поля денормализованной формы
        '''
        {'csrfmiddlewaretoken': ['zeGsl0eB8pmtwkeeI4QPoOpxNCtZGdTgcfDjMWs6ZbPEjDN3pR66QfMaQGjUGy2M'],
         'states.delivered.shlippe': ['0'], 'states.taken.shlippe': ['0'], 'states.consumption.shlippe': ['0'],
         'states.issued.shlippe': ['0'], 'states.delivered.zn_dust': ['0'], 'states.taken.zn_dust': ['0'],
         'stages.zn_dust.1st': ['0'], 'stages.zn_dust.cd': ['0'], 'stages.zn_dust.2st': ['0'],
         'stages.zn_dust.3st': ['0'], 'states.issued.zn_dust': ['0'], 'states.delivered.mg_ore': ['0'],
         'states.taken.mg_ore': ['0'], 'states.consumption.mg_ore': ['0'], 'states.issued.mg_ore': ['0'],
         'states.delivered.magnaglobe': ['0'], 'states.taken.magnaglobe': ['0'], 'tates.consumption.magnaglobe': ['0'],
         'states.issued.magnaglobe': ['0'], 'states.delivered.fe_shave': ['0323'], 'states.taken.fe_shave': ['0'],
         'states.consumption.fe_shave': ['0'], 'states.issued.fe_shave': ['0'], 'fence_state': ['fdgdfg']} >
         '''

        modelDelivered = {
                  'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
                  'fence_state': request.POST['fence_state'],
                  'time': datetime.datetime.now()
                  }

        modelDelivered['shlippe'] = request.POST['states.delivered.shlippe']
        modelDelivered['zn_dust'] = '1'
        modelDelivered['mg_ore'] = '1'
        modelDelivered['magnaglobe'] = '1'
        modelDelivered['fe_shave'] = '1'
        modelDelivered['state'] = 'delivered'
        modelDelivered['stage'] = 'total'
        modelDelivered['journal'] = '1'



        formReagents = ReagentsForm(modelDelivered) # Bind data from request.POST into a PostForm

        if formReagents.is_valid():
            formReagents.save()

            return  HttpResponseRedirect('/leaching/ju')
        else:
            print("Not valid\n\n\n")
            print(formReagents.errors)
            # error_messages = formReagents.errors
            cleaned_data = formReagents.cleaned_data


    journal = Journal.objects.all()[0]
    shift  = Shift.objects.all()[0]

    context = {
            'title': "Журнал Экспресс анализа (Заполнение)",
            'subtitle': "Цех выщелачивания",
            'form_title': "Заполнить форму",
            'form_reagents': {
                            'title': 'Реагенты',
                            'fields': formReagents,
                            'name': "form_reagents",
                            'dump': pprint.pformat(formReagents.fields)
            },
            'journal': journal,
            'shift': shift,
            'error_messages': error_messages,
            'data': cleaned_data
    }

    template = loader.get_template('edit.html')
    return HttpResponse(template.render(context, request))


def leaching_jea(request):
    context = {
        'title': "Журнал Экспресс анализа",
        'subtitle': "Цех выщелачивания"
    }
    table1 = {
            'id': 'simple-table-id',
            'title':'Таблица сгустителей',
            'columns': ["Нейтральные сгустители", "1","2","3","4","5","6","7","8","13"],
            'rows' : [
                {
                    'title':'Отстои',
                    'values': ['100',
                    '100',
                    '100',
                    '100',
                    '100',
                    '-',
                    '-',
                    '100',
                    '-']
                },
                {
                    'title':'Ж:Т',
                    'values': [
                        '0.86:1',
                    '1.0:1',
                    '0.66:1',
                    '1.5:1',
                    '1:1',
                    '-',
                    '-',
                    '1.2:1',
                    '0.86:1']
                },
                {
                    'title':'(НС)',
                    'values':['1.0:1',
                    '1.2:1',
                    '1.0:1',
                    '1.8:1',
                    '1:2',
                    '-',
                    '-',
                    '1.5:1',
                    '1.5:1']
                }
            ]
        }

    table2 = {
        'id': 'simple-table-id',
        'title': 'Нагрузки',
        'columns': ["", "I серия", "II серия", "III серия", "IV серия"],
        'rows': [
            {
                'title': 'Нагрузки',
                'values': ['10', '340','23', '654']
            },
            {
                'title': 'Показания счётчика',
                'values': ['10', '340','23', '654']
            },
            {
                'title': 'Бункера ЦВЦО',
                'values': ['10', '340','23', '654']
            },
            {
                'title': 'Силоса ОЦ',
                'values': ['10', '340','23', '654']
            },
            {
                'title': 'Бункера ОЦ',
                'values': ['10', '340','23', '654']
            },
        ]
    }

    baki = {
        'id': 'simple-table-id',
        'title': 'Баки готовой продукции',
        'columns': ["№ Бака ", "Кадмий", "Медь", "Кобальт", "Сурьма","Железо","В:T","Уд. вес","Норма", "Факт", "Коррекция", "Мастер"],

        'rows': [
            {
                'title': '3',
                'values': ['0.5', '0.08', '0.5', '0.005', '40','-', '1405','-','-','нет','Молдабеков']
            },
            {
                'title': '4',
                'values': ['0.5', '0.08', '0.5', '0.005', '40', '-', '1405', '-', '-', 'нет', 'Молдабеков']
            },
            {
                'title': '5',
                'values': ['0.5', '0.08', '0.5', '0.005', '40', '-', '1405', '-', '-', 'нет', 'Молдабеков']
            },
        ]
    }

    table4 = {
        'id': 'simple-table-id',
        'title': 'Откачено',
        'columns': [" ", " "],

        'rows': [
            {
                'title': 'Выход ТВ',
                'values': ['-']
            },
            {
                'title': 'Пульпы в ЦВЦК, м3',
                'values': ['338.6']
            },
            {
                'title': 'Медного кека',
                'values': ['-']
            },
            {
                'title': 'Cd губка',
                'values': ['6т. 220м']
            },
            {
                'title': 'Отработ. в ЦВОЦ',
                'values': ['900']
            },
            {
                'title': 'Богато-кадмиевого',
                'values': ['220']
            },
            {
                'title': 'Нейтрального ХМЦ',
                'values': ['ЦВО 25']
            },
            {
                'title': 'Пульпа, м3',
                'values': ['11.5']
            },
        ]
    }

    table5 = {
        'id': 'simple-table-id',
        'title': 'Принято',
        'columns': [" ", " "],
        'rows': [
            {
                'title': 'Фильтрат ЦВЦК, Ж:Т',
                'values': ['-']
            },
            {
                'title': 'Уд. вес',
                'values': ['1.375']
            },
            {
                'title': 'Железистого из ЦВОЦ',
                'values': ['900']
            },
            {
                'title': 'Fe р-р',
                'values': ['-']
            },
            {
                'title': 'Богато-кадмиевого',
                'values': ['240']
            },
        ]
    }

    probnik = {
        'id': 'simple-table-id',
        'title': 'Принято',
        'columns': ["Время", "Cd", "Cu"],
        'rows': [
            {
                'values': ['','']
            },
            {
                'values': ['','']
            },
            {
                'values': ['','']
            },
            {
                'values': ['','']
            },
            {
                'values': ['','']
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

    oxrana = {
        'id': 'simple-table-id',
        'title': 'Самоохарана',
        'columns': ['',"Обход", "Примечание"],
        'rows': [
            {
                'values': ['9:00 замечаний нет','','']
            },
            {
                'values': ['9:00 замечаний нет','','']
            },
            {
                'values': ['9:00 замечаний нет','','']
            },
        ]
    }

    sgustiteli = {
        'title': 'Сгустители',
        'columns': ['', "Обход", "Примечание"],
        'rows': [
            {
                'values': ['1', '2', '3','4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15','16','17', '18']
            },
            {
                'values': ['1', '2', '3','4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15','16','17', '18']
            },
            {
                'values': ['1', '2', '3','4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15','16','17', '18']
            },
        ]
    }

    apparat = {
        'title': 'Аппаратчик - гидрометаллург',
        'columns': ['1 Манн', "4 Манн"],
        'rows': [
            {
                'title': '',
                'values': ['1,5', '2', '3', '4', '5', '6', '7', '8']
            },
            {
                'title': '',
                'values': ['1,5', '2', '3', '4', '5', '6', '7', '8']
            },
            {
                'title': '',
                'values': ['1,5', '2', '3', '4', '5', '6', '7', '8']
            }
        ]
    }

    bchc = {
        'title': 'BCHC',
        'columns': ['BCHC', "Ларокс","Очищенный раствор"],
        'level2': ["Кобальт Co","Сурьма", "Медь", "Кадмий", "Твердое После 1ст", "pH (BCHC)", "Железо", "As", "Твёрдое ", "Уд. вес",
                   "Кобальт", "Сурьма", "Кадмий", "Твердое", "pH","Кадмий", "Кобальт", "Сурьма", "Медь", "Железо",
                   "Выход по току", "Уд. вес", "Норма", "Факт", "Несоответствие", "Коррекция", "Мастер"],
        'rows': [
            {
                'title': '',
                'values': ['1,5', '2', '3', '4', '5', '6', '7', '8']
            },
            {
                'title': '',
                'values': ['1,5', '2', '3', '4', '5', '6', '7', '8']
            },
            {
                'title': '',
                'values': ['1,5', '2', '3', '4', '5', '6', '7', '8']
            }
        ]
    }

    context = {
        'table1': table1,
        'table2': table2,
        'baki': baki,
        'table4': table4,
        'table5': table5,
        'probnik': probnik,
        'oxrana': oxrana,
        'sgustiteli': sgustiteli,
        'apparat': apparat,
        'bchc': bchc

    }



    template = loader.get_template('react-table.html')
    return HttpResponse(template.render(context, request))
