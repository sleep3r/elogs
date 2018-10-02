import json

from pywebpush import webpush, WebPushException
from cacheops import cached_view_as

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.views.generic.list import ListView

from e_logs.common.messages_app.models import Message, UserSubscription
from e_logs.core.utils.deep_dict import DeepDict
from e_logs.core.utils.errors import AccessError
from e_logs.core.utils.webutils import model_to_dict, logged, process_json_view
from e_logs.common.all_journals_app.services.context_creator import get_context



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
        context = get_context(self.request, page=None)
        return context


class MessagesSubscription(LoginRequiredMixin, View):
    def post(self, request):
        sub = request.POST.get('registration_data')
        if sub:
            UserSubscription.objects.create(user=request.user.employee,
                                            subscription=sub)
            return JsonResponse({"status":1})
        else:
            return JsonResponse({"status":0})

def push_notification(user_id):
    user_subscriptions = UserSubscription.objects.filter(user_id=user_id)
    for subscription in user_subscriptions:
        data = json.dumps({
        'title': 'Hello',
        'body': 'World!',
    })
        try:
            webpush(
                subscription_info=json.loads(subscription.subscription),
                data=data,
                vapid_private_key='./private_key.pem',
                vapid_claims={
                    'sub': 'mailto:inframine@inframine.io',
                }
            )
        except WebPushException as ex:
            print('I can\'t do that: {}'.format(repr(ex)))
            print(ex)
            # Mozilla returns additional information in the body of the response.
            if ex.response and ex.response.json():
                extra = ex.response.json()
                print('Remote service replied with a {}:{}, {}',
                      extra.code,
                      extra.errno,
                      extra.message
                      )