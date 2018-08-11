import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView

from e_logs.common.all_journals_app.models import Cell, Comment
from e_logs.common.messages_app.models import Message
from e_logs.common.all_journals_app.views import get_or_create_cell
from e_logs.core.utils.deep_dict import DeepDict
from e_logs.core.utils.errors import AccessError
from e_logs.core.utils.webutils import model_to_dict, logged


class MessageView(LoginRequiredMixin, View):

    @logged
    def get(self, request):
        res = DeepDict()
        res['messages'] = {}
        for m in Message.objects.filter(is_read=False, addressee=self.request.user.employee):
            res['messages'][m.id] = model_to_dict(m)
        return res

    @logged
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


class MessagesList(LoginRequiredMixin, ListView):
    model = Message
    context_object_name = 'messages'
    template_name = 'messages_list.html'

    @logged
    def get_queryset(self):
        return self.model.objects.filter(addressee=self.request.user.employee)

    @logged
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@csrf_exempt
@login_required
@logged
def add_critical(request):
    if request.is_ajax() and request.method == 'POST':
        cell = Cell.get(json.loads(request.body)['cell'])
        if cell:
            message = json.loads(request.body)['message']
            message['sendee'] = request.user.employee
            Message.add(cell, message, all_users=True)
    return JsonResponse({'status': 1})


@csrf_exempt
@login_required
@logged
def update(request):
    if request.is_ajax() and request.method == 'POST':
        cell = Cell.get(json.loads(request.body)['cell'])
        if cell:
            Message.update(cell)
    return JsonResponse({'status': 1})


@csrf_exempt
@login_required
@logged
def add_comment(request):
    if request.is_ajax() and request.method == 'POST':
        cell_location = json.loads(request.body)['cell_location']
        message = json.loads(request.body)['message']
        employee = request.user.employee
        message['sendee'] = employee

        cell = get_or_create_cell(**cell_location)
        cell.save()

        Comment.objects.create(target=cell, text=message['text'], employee=employee)

        Message.add(cell, message, all_users=True)

    return JsonResponse({"status": 1})
