import json

from django.http import JsonResponse
from django.db import transaction
from django.views import View
from django.views.generic.list import ListView
from django.shortcuts import render

from e_logs.common.login_app.models import Employee
from e_logs.common.messages_app.models import Message
from e_logs.common.all_journals_app.models import CellValue, JournalPage
from e_logs.common.messages_app.services import messages

from e_logs.core.utils.deep_dict import deep_dict
from e_logs.core.utils.errors import AccessError
from e_logs.core.utils.webutils import model_to_dict

class MessageView(View):

    def getCell(self, request):
        journal_page = request.POST.get('journal_page', None)
        table_name = request.POST.get('table_name', None)
        field_name = request.POST.get('field_name', None)
        row_index = request.POST.get('index', None)
        cell = messages.get_or_none(CellValue, journal_page = journal_page, table_name = table_name, index = row_index, field_name = field_name)
        return cell

    @staticmethod    
    def getLinkToJournal(cell):
        j_page = cell.journal_page
        journal_name = j_page.journal_name
        plant_name = j_page.plant.name
        field_name = cell.field_name.replace("_comment", "")
        return f'/{plant_name}/{journal_name}?page_mode=edit&highlight={field_name}_{cell.index}#table_id_{cell.table_name}">{field_name}'

    def create(self, request, type, cell, text, addressee, link):
        new_msg = Message(
                  sendee = request.user.employee,
                  addressee=addressee,
                  type=type,
                  text=text,
                  cell_field_name=cell.field_name,
                  cell_table_name=cell.table_name,
                  row_index=cell.index,
                  cell_journal_page=cell.journal_page_id,
                  cell_link = link)
        new_msg.save()

    def update(self, cell):
        msgs = messages.filter_or_none(cell, type, addressee=None)
        if msgs:
            for m in msgs:
                m.is_read = True
                m.save()

    def get(self, request):
        res = deep_dict()
        res['messages'] = {}
        for m in Message.objects.filter(is_read=False, addressee=self.request.user.employee):
            res['messages'][m.id] = model_to_dict(m)
        return res

    def post(self, request, crud, type=None):
        cell = self.getCell(request)
        if crud == 'create':

            if type == 'critical_value':
                value = request.POST.get('field_value', None)
                if value:
                    m_link = self.getLinkToJournal(cell)
                    for emp in messages.get_addressees(all=True):
                        msg = messages.filter_or_none(cell, type, emp)
                        if msg:
                            with transaction.atomic():
                                for m in msg:
                                    m.text = value
                                    m.save()
                        else:
                            self.create(request,type, cell, value, emp, m_link)
                else:
                    self.update(cell)


            if type == 'comment':
                comment_text = request.POST.get('comment_text', None)
                if comment_text:
                    m_link = self.getLinkToJournal(cell)
                    for emp in messages.get_addressees(all=True):
                        msg = messages.filter_or_none(cell, type, emp)
                        if msg:
                            with transaction.atomic():
                                for m in msg:
                                    m.text = comment_text
                                    m.save()
                        else:
                            self.create(request, type, cell, comment_text, emp, m_link)
                else:
                    self.update(cell)


        if crud == 'read':
            msg_id = json.loads(request.POST.get('ids[]')) or 0
            msg = Message.objects.get(id=int(msg_id))
            if msg.addressee == request.user.employee:
                msg.is_read = True
                msg.save()
            else:
                raise AccessError(
                    message="Попытка отметить чужое сообщение как прочитанное")


        if crud == 'update':
            self.update(cell)

        return JsonResponse({"result": 1})


class MessagesList(ListView):
    model = Message
    paginate_by = 10
    context_object_name = 'messages'
    template_name = 'messages_list.html'

    def get_queryset(self):
        return self.model.objects.filter(addressee=self.request.user.employee)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
