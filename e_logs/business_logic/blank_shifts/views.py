import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from e_logs.business_logic.services import SetLimitedAccess


@csrf_exempt
def set_limited_access_employee_list(request):
    if request.method == "POST":
        # data = json.loads(request.body)

        data = {"shift_id":104,
                "time":{"hours":1},
                "emp_id_list":[17,20,]}

        SetLimitedAccess.execute(**data)

    return JsonResponse({"status":1})




