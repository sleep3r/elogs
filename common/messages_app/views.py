import json

from django.http import JsonResponse
from django.views import View
from django.template.loader import render_to_string
from django.shortcuts import render
from utils.deep_dict import deep_dict
from utils.webutils import process_json_view, generate_csrf, model_to_dict, set_cookie
from login_app.models import Message, Employee
from common.all_journals_app.models import CellValue
from common.messages_app.services import messages

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
        adding_table_name = request.POST.get('table_name', None)
        adding_field_name = request.POST.get('field_name', None)
        adding_row_index = request.POST.get('index', None)
        adding_journal_page = request.POST.get('journal_page', None)
        adding_field_value = request.POST.get('field_value', None)
        if adding_field_value:
            for emp in messages.get_addressees(all=True):
                msg = messages.filter_or_none(Message,type='critical_value',
                        addressee=emp, 
                        cell_field_name = adding_field_name,
                        cell_table_name = adding_table_name,
                        row_index = adding_row_index,
                        cell_journal_page = adding_journal_page,
                        is_read=False)
                
                if msg:
                    for m in msg:
                        m.text = f'Петрович {request.user.employee.name} ввел в поле {adding_field_name} некорректное значение {adding_field_value}'
                        m.save()

                else:
                    new_msg = Message(
                        type='critical_value', 
                        text=f'Петрович {request.user.employee.name} ввел в поле {adding_field_name} некорректное значение {adding_field_value}',
                        addressee=emp,
                        cell_field_name=adding_field_name,
                        cell_table_name=adding_table_name,
                        row_index=adding_row_index,
                        cell_journal_page=adding_journal_page,)
                    new_msg.save()
        else:
            messages.check_del_string(adding_table_name, adding_journal_page, adding_row_index)
            
        return JsonResponse({"result": 1})

class DelMessagesView(View):
    def post(self, request):
        deleting_table_name = request.POST.get('table_name', None)
        deleting_field_name = request.POST.get('field_name', None)
        deleting_row_index = request.POST.get('index', None)
        deleting_journal_page = request.POST.get('journal_page', None)

        messages_on_delete = messages.filter_or_none(Message, is_read = False, 
                                                     type='critical_value', 
                                                     cell_field_name=deleting_field_name, 
                                                     cell_journal_page=deleting_journal_page, 
                                                     cell_table_name=deleting_table_name, 
                                                     row_index=deleting_row_index)
        if messages_on_delete:
            for message in messages_on_delete:
                message.is_read = True
                message.save()
