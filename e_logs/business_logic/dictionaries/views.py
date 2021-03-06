import json

from django.http import JsonResponse
from django.urls import URLResolver
from django.urls.resolvers import RegexPattern
from django.views import View

from e_logs.business_logic.dictionaries.models import ConcentrateDict, EquipmentDict
from e_logs.common.login_app.models import Employee
from e_logs.core.models import CustomUser
from e_logs.core.views import LoginRequired


class DictionariesApi(View):
    def get(self, request):
        urls = []
        resolver = URLResolver(RegexPattern(r'^/'), 'e_logs.business_logic.dictionaries.urls')
        for url in filter(lambda x: isinstance(x[0], str), list(resolver.reverse_dict.items())):
            link = '/api/bl/dicts/' + url[1][0][0][0]
            urls.append({"title": url[0], "link": link, 'name':link.split('/')[-2]})

        return JsonResponse(urls, safe=False)


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


class UsernamesAPI(View):
    def get(self, request):
        name = request.GET.get('name', None)
        if name:
            return JsonResponse([user.username for user in
                                 CustomUser.objects.filter(username__contains=name)] +
                                [user.email for user in
                                 CustomUser.objects.filter(email__contains=name)],
                                    safe=False)
        else:
            return JsonResponse([], safe=False)


class ConcentratesAPI(View):
    def get(self, request):
        name = request.GET.get('name', None)
        if name:
            return JsonResponse([concentrate.name for concentrate in
                                 ConcentrateDict.objects.filter(name__contains=name)],
                                    safe=False)
        else:
            return JsonResponse([], safe=False)


class EquipmentAPI(View):
    def get(self, request):
        name = request.GET.get('name', None)
        if name:
            return JsonResponse([equipment.name for equipment in
                                 EquipmentDict.objects.filter(name__contains=name)],
                                    safe=False)
        else:
            return JsonResponse([], safe=False)


class EmailsAPI(View):
    def get(self, request):
        name = request.GET.get('name', None)
        if name:
            return JsonResponse([user.email for user in
                                 CustomUser.objects.filter(email__contains=name)],
                                    safe=False)
        else:
            return JsonResponse([], safe=False)
