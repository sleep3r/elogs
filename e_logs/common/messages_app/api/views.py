import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View

from e_logs.common.messages_app.models import Message
from e_logs.core.utils.errors import AccessError
from e_logs.core.utils.webutils import model_to_dict, logged


class MessagesAPI(LoginRequiredMixin, View):
    @logged
    def get(self, request):
        res = {}
        for m in self.request.user.employee.unread_messages():
            res[m.id] = model_to_dict(m)
        return JsonResponse(res)

    @logged
    def put(self, request):
        msg_ids = request.POST.get('id')
        if msg_ids:
            msg_ids = msg_ids.split(',')
            for id in msg_ids:
                msg = Message.objects.get(id=int(id))
                if msg.addressee == request.user.employee:
                    msg.is_read = True
                    msg.save()
                else:
                    raise AccessError(
                        message="Попытка отметить чужое сообщение как прочитанное")

            return JsonResponse({"status": 1})

        return JsonResponse({"status": 0})


class MessagesList(LoginRequiredMixin, View):
    def get(self, request):
        res = {}
        qs = Message.objects.filter(addressee=request.user.employee).order_by("-created")
        for message in qs:
            res[message.id] = model_to_dict(message)

        return JsonResponse(res)
