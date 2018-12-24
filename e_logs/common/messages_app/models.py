import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet, Q
from django.utils import timezone
from pywebpush import webpush, WebPushException

from e_logs.common.login_app.models import Employee
from e_logs.core.utils.webutils import filter_or_none, StrAsDictMixin, user_to_response


class Message(StrAsDictMixin, models.Model):
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')
    created = models.DateTimeField(default=timezone.now, blank=True)

    cell = models.ForeignKey('all_journals_app.Cell', on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=32, verbose_name='Тип сообщения',
                            default='', choices=(('critical_value', 'Критическое значение'),
                                                 ('comment', 'Замечание'),
                                                 ('set_mode', "Режим"),
                                                 ('blank_journal', "Пустой журнал"),), )
    text = models.TextField(verbose_name='Текст сообщения')

    sendee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='messages_sendee')
    addressee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='messages_addressee')

    link = models.URLField(max_length=1024, verbose_name='Ссылка на ячейку', default="#", null=True)

    @staticmethod
    def get_recepients(message, all_users=False, positions=None, uids=None, plant_name=None):

        recipients = []

        if uids:
            recipients = []
            recipients.extend(Employee.objects.filter(id__in=uids).exclude(name=message['sendee']))

        if positions:
            recipients = []
            for p in positions:
                recipients.extend(Employee.objects.
                                  filter(plant=plant_name if plant_name else None, position=p).
                                  exclude(name=message['sendee']))
        if plant_name:
            recipients = []
            recipients.extend(
                Employee.objects.filter(Q(plant=plant_name) | Q(plant=None)).exclude(name=message['sendee']))

        if all_users:
            recipients = []
            recipients.extend(Employee.objects.all().exclude(name=message['sendee']))

        return recipients

    @staticmethod
    def add(message, cell=None, all_users=False, positions=None, uids=None, plant_name=None):
        """
        TODO: add builder class
        'message': {
                    'text': "some text",
                    'link': Optional[URI],
                    'type': "message type",
                    'sendee': Employee or None,
                    'created': Optional[datetime]
                }
        """
        recipients = Message.get_recepients(message, all_users, positions, uids, plant_name)

        text = message.pop('text', '')

        layer = get_channel_layer()

        for emp in recipients:
            msg = filter_or_none(Message, **message,
                                 addressee=emp, cell=cell, type__in=('comment', 'critical_value')).first()
            if msg and msg.type == 'critical_value':
                msg.text = text
                msg.save()
            else:
                Message.objects.create(**message, addressee=emp, cell=cell, text=text)
                data = {
                    "type": message['type'],
                    "shift_id": cell.group.id if cell else None,
                    "cell": {
                        'table_name': cell.table.name,
                        'field_name': cell.field.name,
                        'index': cell.index
                    } if cell else None,
                    "sendee": user_to_response(message['sendee']),
                    "text": text,
                    "created": message.get('created', timezone.localtime().isoformat())
                }
                async_to_sync(layer.group_send)(f'user_{emp.id}', {"type": "send_message", "text": json.dumps(data)})

                # Message.push_notification(title='E-LOGS', body='Новое сообщение', user_id=emp.id)

    @staticmethod
    def push_notification(title, body, user_id):
        user_subscriptions = UserSubscription.objects.filter(user_id=user_id)
        for subscription in user_subscriptions:
            data = json.dumps({
                'title': title,
                'body': body,
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
                if ex.response and ex.response.json():
                    extra = ex.response.json()
                    print('Remote service replied with a {}:{}, {}',
                          extra.code,
                          extra.errno,
                          extra.message)

    @staticmethod
    def update(cell):
        messages = filter_or_none(Message, cell=cell)
        if messages:
            for message in messages:
                message.is_read = True
                message.save()

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        indexes = [
            models.Index(fields=['is_read', 'addressee']),
            models.Index(fields=['addressee']),
            models.Index(fields=['created']),
        ]

    @staticmethod
    def get_unread(employee) -> QuerySet:
        return Message.objects.filter(is_read=False, addressee=employee)


class UserSubscription(models.Model):
    subscription = models.CharField(max_length=500)
    user = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='subscriptions')
