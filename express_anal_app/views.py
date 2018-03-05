import json

from django.http import HttpResponse
from django.http import HttpResponseRedirect


from django.template import loader
# forms
from django import forms
from django.forms import ModelForm


# -------------- django web forms -----------------------
from express_anal_app.models import DenserAnal


class PostForm(forms.Form):
    content = forms.CharField(max_length=255)
    created_at = forms.DateTimeField()

class DenserForm(ModelForm):
    class Meta:
        model = DenserAnal
        fields = ['point','sink','ph', 'cu', 'fe', 'liq_sol']

# ------------- end forms -----------------------------

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

def electrolysis(request):
    context = {
        'title': "Журнал Экспресс анализа",
        'subtitle': "Цех выщелачивания"
    }
    template = loader.get_template('journal.html')
    return HttpResponse(template.render(context, request))

def leaching_ju(request):
    context = {
        'title': "Журнал учёта ",
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

# def electrolysis(request):
#     context = {
#         'title': "Реактивная табличка",
#         'subtitle': "Цех Электроиза"
#     }
#     template = loader.get_template('react-table.html')
#     return HttpResponse(template.render(context, request))

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
    dump = ''
    if request.method == 'GET':
        form = DenserForm()
    else:
        form = DenserForm(request.POST) # Bind data from request.POST into a PostForm
        if form.is_valid():
            dump = form.cleaned_data['ph']
            form.save()
            return HttpResponseRedirect

    context = {
        'title': "Журнал Экспресс анализа (Edit)",
        'subtitle': "Цех выщелачивания",
        'form': form,
        'dump': dump
    }
    template = loader.get_template('journal-edit.html')
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
