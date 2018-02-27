import json

from django.http import HttpResponse
from django.template import loader

def index(request):
    context = {
        'hello_list': ['World', 'Darling', 'Inframine', 'Goodbye']
    }
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))

