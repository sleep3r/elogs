from django.shortcuts import render
from cacheops import cached_view_as
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.views.generic.list import ListView

from e_logs.common.messages_app.models import Message
from e_logs.core.utils.deep_dict import DeepDict
from e_logs.core.utils.errors import AccessError
from e_logs.core.utils.webutils import model_to_dict, logged, process_json_view


# Create your views here.
class GraphsListView(LoginRequiredMixin, View):
    @logged
    def post(self, request):
        pass
        return JsonResponse({"result": 1})


class GraphView(LoginRequiredMixin, View):
    @logged
    def post(self, request):
        pass
        return JsonResponse({"result": 1})
