import json
from datetime import timedelta

from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from e_logs.business_logic.services import SetMode, SetLimitedAccess
from e_logs.common.all_journals_app.models import Shift
from e_logs.common.login_app.models import Employee
from e_logs.core.models import Setting
from e_logs.common.all_journals_app.tasks import end_of_limited_access, send_deferred_message

@csrf_exempt
def set_limited_access_employee_list(request):
    if request.method == "POST":
        # data = json.loads(request.body)

        data = {"shift_id":104,
                "time":{"hours":1},
                "emp_id_list":[17,20,]}

        SetLimitedAccess.execute(**data)

    return JsonResponse({"status":1})




