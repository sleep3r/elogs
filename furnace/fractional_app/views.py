from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader

@login_required
def index(request):
    template = loader.get_template('spa-index.html')
    return HttpResponse(template.render())
    # context = {
    #     'hello_list': ['World', 'Darling', 'Inframine', 'Goodbye'],
    #     'tile_counts': {'total': '31337'},
    #     'system_messages': [
    #         {'title': _("Температура кипящего слоя превысила критический показатель"), 'time': "12:33"},
    #         {'title': _("Всё хорошо"), 'time': "10:33"},
    #         {'title': _("Надо пошурудить в печи"), 'time': "08:00"}
    #     ],
    #     'user_name': str(request.user.employee),
    #     'notifications': [{
    #         'type': 'asd',
    #         'message': "Здорова, как делишки?",
    #         'id': -1
    #     }, {
    #         'type': 'asd',
    #         'message': "Здорова, как делишки? Здорова, как делишки? Здорова, как делишки? Здорова, как делишки? Здорова, как делишки?",
    #         'id': -2
    #     }, {
    #         'type': 'asd',
    #         'message': "Здорова, как делишки?",
    #         'id': -3
    #     }]
    # }

