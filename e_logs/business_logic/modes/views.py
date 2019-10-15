import json

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from e_logs.business_logic.modes.models import Mode, FieldConstraints
from e_logs.business_logic.services import SetMode, UpdateMode
from e_logs.core.utils.webutils import logged, get_or_none
from e_logs.core.views import LoginRequired



class ModeApi(LoginRequired, View):
    def post(self, request):
        data = json.loads(request.body)
        data['sendee'] = request.user.employee
        mode = SetMode.execute(data)

        return JsonResponse({"status": 1, "id": mode.id})

    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        UpdateMode.execute(data)

        return JsonResponse({"status": 1})

    def get(self, request, *args, **kwargs):
        res = [{
            "id":mode.id,
            "is_active": mode.is_active,
            "message": mode.message,
            "journal":{mode.journal.name:mode.journal.verbose_name},
            "plant": {mode.journal.plant.name:mode.journal.plant.verbose_name},
            "fields": [{
                        "name":constraint.field.name,
                        "table_name": constraint.field.table.name,
                        "min_normal": constraint.min_normal,
                        "max_normal": constraint.max_normal
                        } for constraint in FieldConstraints.objects.filter(mode=mode)]

            } for mode in Mode.objects.all()]

        return JsonResponse(res, safe=False)

@csrf_exempt
def mode_delete(request, *args, **kwargs):
    if request.method == "DELETE":
        mode = get_or_none(Mode, id=kwargs['id'])

        if mode:
            mode.delete()
            return JsonResponse({"status": 1})
        else:
            return JsonResponse({"status": 0})
