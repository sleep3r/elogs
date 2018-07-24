from django.views.decorators.csrf import csrf_exempt
from e_logs.core.utils.webutils import process_json_view, logged
from .feedback import send_feedback


@csrf_exempt
@process_json_view(auth_required=False)
@logged
def send_message(request):
    send_feedback(request.POST)
    return {"result": 1}
