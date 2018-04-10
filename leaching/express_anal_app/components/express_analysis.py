from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.template import loader

@login_required
def express(request):
    context = {
        'js-files': [
            'https://alfa.com/main.js'
        ]
    }

    template = loader.get_template('analysis.html')
    return HttpResponse(template.render(context, request))