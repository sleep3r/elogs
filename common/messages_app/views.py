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
        res = deep_dict()
        res['messages'] = {}
        for m in Message.objects.filter(is_read=False, addressee=self.request.user.employee):
            res['messages'][m.id] = model_to_dict(m)
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

        return JsonResponse({"result": 1})


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
                        m.text = f'<b>{request.user.employee.name}</b> ввел в поле <b>{adding_field_name}</b> некорректное значение {adding_field_value}'
                        m.save()

                else:
                    new_msg = Message(
                        type='critical_value', 
                        text=f'<b>{request.user.employee.name}</b> ввел в поле <b>{adding_field_name}</b> некорректное значение {adding_field_value}',
                        addressee=emp,
                        cell_field_name=adding_field_name,
                        cell_table_name=adding_table_name,
                        row_index=adding_row_index,
                        cell_journal_page=adding_journal_page,)
                    new_msg.save()
        else:
            msgs = messages.filter_or_none(Message, is_read=False,
                                      cell_table_name=adding_table_name,
                                      row_index=adding_row_index,
                                      cell_journal_page=adding_journal_page)
            if msgs:
                for m in msgs:
                    m.is_read = True
                    m.save()
            
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

        return JsonResponse({"result": 1})



class AddComment(View):
    def post(self, request):
        comment_text = request.POST.get('comment_text', None)
        table_name = request.POST.get('table_name', None)
        field_name = request.POST.get('field_name', None)
        row_index = request.POST.get('index', None)
        journal_page = request.POST.get('journal_page', None)
        if comment_text:
            for emp in messages.get_addressees(all=True):
                msg = messages.filter_or_none(Message, type='comment',
                                              addressee=emp,
                                              is_read=False,
                                              cell_table_name=table_name,
                                              cell_field_name=field_name,
                                              cell_journal_page=journal_page,
                                              row_index=row_index)

                if msg:
                    for m in msg:
                        m.text = f'{request.user.employee.name} оставил к таблице {table_name} комментарий: {comment_text}'
                        m.save()

                else:
                    new_msg = Message(
                        type='comment',
                        text=f'{request.user.employee.name} оставил к таблице {table_name} комментарий: {comment_text}',
                        addressee=emp,
                        cell_table_name=table_name,
                        cell_field_name=field_name,
                        cell_journal_page=journal_page,
                        row_index=row_index)
                    new_msg.save()

        else:
            msgs = messages.filter_or_none(Message, is_read=False,
                                           cell_table_name=table_name,
                                           cell_field_name=field_name,
                                           cell_journal_page=journal_page,
                                           row_index=row_index
                                           )
            if msgs:
                for m in msgs:
                    m.is_read = True
                    m.save()
        
        return JsonResponse({"result": 1})
