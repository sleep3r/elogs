from django.views.decorators.csrf import csrf_exempt
from e_logs.core.utils.webutils import process_json_view, logged
from .models import Feedback


@csrf_exempt
@process_json_view(auth_required=False)
@logged
def send_message(request):
    data = request.POST
    fb = Feedback(
        username=data["user"],
        email=data["email"],
        plant=data["plant"],
        journal=data["journal"],
        theme=data["theme"],
        text=data["text"]
    )
    fb.send_feedback()
    fb.save()
    return {"result": 1}
