import json

from django.http import HttpResponse
from django.views import View
from django.template.loader import render_to_string
from django.shortcuts import render
from utils.deep_dict import deep_dict
from utils.webutils import process_json_view, generate_csrf, model_to_dict, set_cookie
from login_app.models import Message, Employee
from common.all_journals_app.models import CellValue
from common.messages_app.services.messages import get_addressees

class GetMessagesView(View):
    def get(self, request):
        result = request.user.employee.has_unreaded()
        res = deep_dict()

        if result:
            res['result'] = result
            res['messages'] = {}
            for m in Message.objects.filter(is_read=False, addressee=Employee.objects.only('user').get(user=self.request.user.id)):
                res['messages'][m.id] = model_to_dict(m)
            return res

        else:
            res['result'] = result
            return res


class ReadMessagesView(View):
    def post(self, request):
        msg_id = json.loads(request.POST.get('ids[]')) or 0
        msg = Message.objects.get(id=int(msg_id))
        if msg.addressee == request.user.employee:
            msg.is_read = True
            msg.save()
        else:
            raise AccessError(
                message="Попытка отметить чужое сообщение как прочитанное")

        return {"status": 0}


class AddMessagesView(View):
    def post(self, request):
        field_name = request.POST.get('while_adding_field_name', None)
        field_value = request.POST.get('while_adding_field_value', None)
        result = False
        if field_name:
                result = True
                for emp in get_addressees(all=True):
                    msg = Message(
                     type='critical_value', text=f'Петрович {request.user.employee.name} ввел в поле {field_name} некорректное значение {field_value}' , addressee=emp)
                    msg.save()
        
        return HttpResponse(
            json.dumps({
                "result": result ,
            }),
            content_type="application/json"
        )
