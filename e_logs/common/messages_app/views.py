import json

from cacheops import cached_view_as
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView

from e_logs.common.all_journals_app.models import Cell, Comment
from e_logs.common.messages_app.models import Message
from e_logs.core.utils.deep_dict import DeepDict
from e_logs.core.utils.errors import AccessError
from e_logs.core.utils.webutils import model_to_dict, logged, process_json_view


class MessageView(LoginRequiredMixin, View):
    @logged
    def get(self, request):
        res = DeepDict()
        res['messages'] = {}
        for m in self.request.user.employee.unread_messages():
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


msg_view = MessageView.as_view()
msg_view = process_json_view(auth_required=False)(msg_view)
msg_view = cached_view_as(Message.objects.filter(is_read=False))(msg_view)


class MessagesList(LoginRequiredMixin, ListView):
    model = Message
    context_object_name = 'messages'
    template_name = 'messages_list.html'
    paginate_by = 10

    @logged
    def get_queryset(self):
        return self.model.objects.filter(addressee=self.request.user.employee).order_by("-created")

    @logged
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@csrf_exempt
@login_required
@logged
def add_comment(request):
    if request.is_ajax() and request.method == 'POST':
        comment_data = json.loads(request.body)
        message = comment_data['message']
        message['sendee'] = request.user.employee
        text = message['text']

        cell = Cell.get_or_create_cell(**comment_data['cell_location'])
        if cell:
            Comment.objects.update_or_create(content_type=ContentType.objects.get_for_model(cell), object_id=cell.id,
                                             defaults={'text': text,
                                                       'employee': request.user.employee})

            Message.add(cell, message, all_users=True)

        return JsonResponse({"status": 1})
