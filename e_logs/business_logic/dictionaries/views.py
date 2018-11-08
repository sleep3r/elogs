import json

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.schemas import get_schema_view

from . import urls
from e_logs.common.login_app.models import Employee
from e_logs.core.utils.webutils import logged, get_or_none
from e_logs.core.views import LoginRequired


def get_resolved_urls(url_patterns):
    url_patterns_resolved = []
    for entry in url_patterns:
        if hasattr(entry, 'url_patterns'):
            url_patterns_resolved += get_resolved_urls(
                entry.url_patterns)
        else:
            url_patterns_resolved.append(entry)
    return url_patterns_resolved

class DictionariesApi(LoginRequired, View):
    def get(self, request, *args, **kwargs):
        pass

get_schema_view()
class AutocompleteAPI(View):
    def get(self, request):
        name = request.GET.get('name', None)
        plant = request.GET.get('plant', None)
        if name and plant:
            return JsonResponse([emp.name for emp in
                                 Employee.objects.filter(name__contains=name,
                                                         user__groups__name__contains=plant.title())],
                                safe=False)
        else:
            return JsonResponse([], safe=False)