import json

from django.http import HttpResponse
from django.views import View
from django.template.loader import render_to_string
from django.shortcuts import render
from utils.deep_dict import deep_dict
from utils.webutils import process_json_view, generate_csrf, model_to_dict, set_cookie
from login_app.models import Message, Employee
from common.all_journals_app.models import CellValue
from leaching.express_anal_app.services import messages
#from common.messages_app.helpers.critical_getter import get_critical_fields


class GetMessagesView(View):
    @staticmethod
    def get_addressees(all=False, positions=None, ids=None, plant=None):
        res = []
        if all:
            return Employee.objects.only('user')
        if positions:
            for p in positions:
                emp = Employee.objects.filter(plant=plant, position=p)
                res.extend(emp)
        if ids:
            for id in ids:
                emp = Employee.objects.get(id=id)
                res.append(emp)

        return res

    def get(self, request):
        #self.check_messages()
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
    def get(self, request):
        
       
        return 