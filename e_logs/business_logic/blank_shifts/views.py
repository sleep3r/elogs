import json
from datetime import timedelta

from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from e_logs.business_logic.services import SetMode
from e_logs.common.all_journals_app.models import Shift
from e_logs.common.login_app.models import Employee
from e_logs.core.models import Setting
from e_logs.common.all_journals_app.tasks import end_of_limited_access, send_deferred_message

@csrf_exempt
def set_limited_access_employee_list(request):
    if request.method == "POST":
        data = json.loads(request.body)
        data = {"shift_id":id,
                "time":{"hours":3},
                "emp_id_list":[1,2,3]}

        page = Shift.objects.get(id=data['shift_id'])

        Setting.of(page)['limited_access_employee_id_list'] = data['emp_id_list']

        end_time = timezone.now() + timedelta(**data['time'])
        end_of_limited_access.apply_async((page.id,), eta=end_time)

        for min in (60, 40, 20):
            send_deferred_message.apply_async(
                ('warning', f'До конца ограниченного доступа осталось {min} минут'),
                eta=end_time-timedelta(minutes=min) )




