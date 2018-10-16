import json

from django.http import JsonResponse
from django.views import View

from e_logs.common.messages_app.models import  UserSubscription
from e_logs.core.views import LoginRequired


class MessagesSubscription(LoginRequired, View):
    def post(self, request):
        sub_info = json.loads(request.body)
        if sub_info:
            UserSubscription.objects.update_or_create(user=request.user.employee,
                                                defaults={"subscription":json.dumps(sub_info)})
            return JsonResponse({"status":1})
        else:
            return JsonResponse({"status":0})
