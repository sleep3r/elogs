import json

from pywebpush import webpush, WebPushException
from cacheops import cached_view_as

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View

from e_logs.common.messages_app.models import  UserSubscription


class MessagesSubscription(LoginRequiredMixin, View):
    def post(self, request):
        sub_info = json.loads(request.body)
        if sub_info:
            UserSubscription.objects.create(user=request.user.employee,
                                            subscription=json.dumps(sub_info))
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
            print(subscription.subscription)
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