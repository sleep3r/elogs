import json
from urllib.parse import parse_qs

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import model_to_dict
from django.http import JsonResponse
from django.views import View

from e_logs.common.messages_app.models import Message
from e_logs.core.utils.errors import AccessError
from e_logs.core.utils.webutils import logged
from e_logs.core.views import LoginRequired


class MessagesAPI(LoginRequired, View):
    @logged
    def get(self, request):
        res = [{
            "id": m.id,
            "created": m.created,
            "is_read": m.is_read,
            "sendee": m.sendee.name,
            "type": m.type,
            "text": m.text,
            "link": m.link,
            "cell": {"plant":m.cell.journal.plant.name,
                     "journal": m.cell.journal.name,
                     "table":m.cell.field.table.name,
                     "field": m.cell.field.name,
                     "index": m.cell.index
                     } if m.cell else None,
        } for m in self.request.user.employee.unread_messages()]

        return JsonResponse(res, safe=False)

    @logged
    def put(self, request):
        qs = parse_qs(request.META['QUERY_STRING'])
        if qs:
            msg_ids = qs['id'][0].split(',')
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


class MessagesList(LoginRequired, View):
    def get(self, request):
        qs = Message.objects.filter(addressee=request.user.employee).order_by("-created")
        res = [{
            "id": m.id,
            "created": m.created,
            "is_read": m.is_read,
            "sendee": m.sendee.name,
            "type": m.type,
            "text": m.text,
            "link": m.link,
            "cell": {"plant": m.cell.journal.plant.name,
                     "journal": m.cell.journal.name,
                     "table": m.cell.field.table.name,
                     "field": m.cell.field.name,
                     "index": m.cell.index
                     } if m.cell else None,
        } for m in qs]

        return JsonResponse(res, safe=False)
