import json

from django.http import HttpResponse
from django.template import loader

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


def leaching_jea(request):
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
