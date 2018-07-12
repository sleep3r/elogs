import json

from django.http import JsonResponse
from django.views import View
from django.template.loader import render_to_string
from django.shortcuts import render
from utils.deep_dict import deep_dict
from utils.errors import AccessError
from utils.webutils import process_json_view, generate_csrf, model_to_dict, set_cookie
from login_app.models import Employee
from common.messages_app.models import Message
from common.all_journals_app.models import CellValue, JournalPage
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
    def getLinkToJournal(self, page_id, table_name, field_name, row_index):
        j_page = JournalPage.objects.get(id=page_id)
        journal_name = j_page.journal_name
        plant_name = j_page.plant.name

        return f'<a href="/{plant_name}/{journal_name}?page_mode=edit&highlight={field_name}_{row_index}#table_id_{table_name}">{field_name}</a>'

    def post(self, request):
        table_name = request.POST.get('table_name', None)
        field_name = request.POST.get('field_name', None)
        row_index = request.POST.get('index', None)
        journal_page_id = request.POST.get('journal_page', None)
        adding_field_value = request.POST.get('field_value', None)

        if adding_field_value:
            for emp in messages.get_addressees(all=True):
                msg = messages.filter_or_none(Message, type='critical_value',
                        addressee=emp,
                        cell_field_name = field_name,
                        cell_table_name = table_name,
                        row_index = row_index,
                        cell_journal_page = journal_page_id,
                        is_read=False)


                msg_text = f'<b>{request.user.employee.name}</b> ввел в поле {self.getLinkToJournal(journal_page_id,  table_name, field_name, row_index)} некорректное значение {adding_field_value}'

                if msg:
                    for m in msg:
                        m.text = msg_text
                        m.save()

                else:
                    new_msg = Message(
                        type='critical_value',
                        text=msg_text,
                        addressee=emp,
                        cell_field_name=field_name,
                        cell_table_name=table_name,
                        row_index=row_index,
                        cell_journal_page=journal_page_id,)
                    new_msg.save()
        else:
            msgs = messages.filter_or_none(Message, is_read=False,
                                      cell_table_name=table_name,
                                      row_index=row_index,
                                      cell_journal_page=journal_page_id)
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
