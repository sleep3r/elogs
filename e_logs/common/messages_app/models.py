import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone

from e_logs.common.login_app.models import Employee
from e_logs.core.utils.webutils import filter_or_none, StrAsDictMixin, get_or_none


class Message(StrAsDictMixin, models.Model):
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')
    created = models.DateTimeField(default=timezone.now, blank=True)

    cell = models.ForeignKey('all_journals_app.Cell', on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=1024, verbose_name='Тип сообщения',
                            default='', choices=(('critical_value', 'Критическое значение'),
                                                 ('comment', 'Замечание'),
                                                 ('set_mode', "Режим"),
                                                 ('blank_journal', "Пустой журнал"),),)
    text = models.TextField(verbose_name='Текст сообщения')

    sendee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='messages_sendee')
    addressee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='messages_addressee')

    link = models.URLField(max_length=1024, verbose_name='Ссылка на ячейку', default="#", null=True)

    @staticmethod
    def add(cell, message, all_users=False, positions=None, uids=None, plant=None):
        '''
        'message': {
                    'text': "some text",
                    'link': Optional[URI],
                    'type': "message type",
                    'sendee': Employee or None,
                }
        '''

        if not all_users and positions is None and uids is None and plant is None:
            raise ValueError

        recipients = []

        if uids:
            recipients = []
            for uid in uids:
                recipients.extend(Employee.objects.get(id=uid).
                                  exclude(name=message['sendee']).cache())
        if positions:
            recipients = []
            for p in positions:
                recipients.\
                    extend(Employee.objects.
                           filter(plant=plant if plant else None, position=p).
                           exclude(name=message['sendee']).cache())
        if all_users:
            recipients = []
            recipients.extend(Employee.objects.all().exclude(name=message['sendee']).cache())

        text = message.pop('text', '')

        layer = get_channel_layer()

        for emp in recipients:
            msg = get_or_none(Message, **message,
                              addressee=emp, cell=cell, type__in=('comment', 'critical_value'))
            if msg:
                msg.text = text
                msg.save()
            else:
                Message.objects.create(**message, addressee=emp, cell=cell, text=text)
                async_to_sync(layer.group_send)\
                    (f'user_{emp.id}', {"type": "message.send",
                                       "text": json.dumps({
                                           'cell': cell.field.name if cell else None,
                                           'sendee': message['sendee'].name if message['sendee'] else '',
                                           'text': text})})

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
    def get_addressees(all_users=False, positions=None, eids=None, plant=None):
        """Отдает список адресатов"""

        res = []
        if all_users:
            return Employee.objects.only('user')
        if positions:
            for p in positions:
                emp = Employee.objects.filter(plant=plant, position=p).cache()
                res.extend(emp)
        if eids:
            for eid in eids:
                emp = Employee.objects.get(id=eid)
                res.append(emp)

        return res

    @staticmethod
    def get_unread(employee) -> QuerySet:
        return Message.objects.filter(is_read=False, addressee=employee)