import json
from datetime import timedelta

from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from e_logs.business_logic.modes.services import SetMode
from e_logs.common.login_app.models import Employee
from e_logs.core.utils.webutils import process_json_view


@csrf_exempt
def create_mode(request):
    if request.method == 'GET':# POST
    #     data = json.loads(request.body)
    #     data['sendee'] = request.user.employee
    #     SetMode.execute(**data)
    #     return {"status":1}
    #
        SetMode.execute({"beginning":timezone.now(),
            "end":timezone.now() + timedelta(minutes=3),
            "message":"12345",
            'sendee':Employee.objects.get(name='inframine'),
            "fields":[
                {"name":"wagon_num", "table_name":"big","min_normal":228, "max_normal":1488},
            ]})

        return JsonResponse({"status":1})
