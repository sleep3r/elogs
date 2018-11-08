import json

from django.http import JsonResponse
from django.urls import URLResolver
from django.urls.resolvers import RegexPattern
from django.views import View

from e_logs.common.login_app.models import Employee
from e_logs.core.views import LoginRequired


class DictionariesApi(LoginRequired, View):
    def get(self, request):
        urls = {}
        resolver = URLResolver(RegexPattern(r'^/'), 'e_logs.business_logic.dictionaries.urls')
        for url in filter(lambda x: isinstance(x[0], str), list(resolver.reverse_dict.items())):
            urls[url[0]] = '/api/bl/dicts/' + url[1][0][0][0]

        return JsonResponse(urls)


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