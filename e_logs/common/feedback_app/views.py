from django.views.decorators.csrf import csrf_exempt
from e_logs.core.utils.webutils import process_json_view, logged
from .models import Feedback
from e_logs.common.login_app.models import Employee
import hashlib
import os


@csrf_exempt
@process_json_view(auth_required=False)
@logged
def send_message(request):
    data = request.POST
    filenames = []
    if request.FILES:
        for key in request.FILES:
            file = request.FILES[key]
            content = file.read()
            hash = hashlib.md5(content).hexdigest()
            dirpath = os.path.join(os.path.dirname(__file__), "media")
            filepath = os.path.join(dirpath, hash)
            with open(filepath, "wb") as f:
                f.write(content)
            filenames.append(filepath)

    user = request.user
    employee = Employee.objects.get(user=user)

    fb = Feedback(
        username=user.username,
        email=user.email,
        plant=employee.plant,
        url=data["url"],
        filenames=",".join(filenames),
        theme=data["title"],
        text=data["message"]
    )

    # try:
    fb.send_feedback()
    # except Exception as e:
    #     print(e)
    fb.save()
    return {"result": 1}
