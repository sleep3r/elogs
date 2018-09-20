import json
from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils import timezone
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.generic import ListView

from e_logs.business_logic.modes.models import Mode, FieldConstraints
from e_logs.business_logic.services import SetMode, UpdateMode
from e_logs.common.all_journals_app.services.context_creator import get_context
from e_logs.common.login_app.models import Employee
from e_logs.core.utils.webutils import logged, get_or_none


class ModeView(LoginRequiredMixin, TemplateView):
    template_name = 'modes.html'

    def get_context_data(self, *args, **kwargs):
        context = get_context(self.request, page=None)
        return context


class ModeApi(LoginRequiredMixin, View):
    def post(self, request):
        data = json.loads(request.body)
        data['sendee'] = request.user.employee
        SetMode.execute(data)

        return JsonResponse({"status": 1})

    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        UpdateMode.execute(data)

        return JsonResponse({"status": 1})

    def delete(self, request, *args, **kwargs):
        mode = get_or_none(Mode, id=request.body['id'])
        if mode:
            mode.delete()

    def get(self, request, *args, **kwargs):
        res = [{
            "id":mode.id,
            "is_active": mode.is_active,
            "message": mode.message,
            "fields": [{
                        "name":constraint.field.name,
                        "table_name": constraint.field.table.name,
                        "min_normal": constraint.min_normal,
                        "max_normal": constraint.max_normal
                        } for constraint in FieldConstraints.objects.filter(mode=mode)]

            } for mode in Mode.objects.all().order_by('is_active')]

        return JsonResponse(res, safe=False)