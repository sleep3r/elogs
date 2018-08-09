from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from e_logs.common.login_app.models import Employee
from e_logs.core.utils.webutils import filter_or_none


class Message(models.Model):
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')
    created = models.DateTimeField(default=timezone.now, blank=True)

    cell = models.ForeignKey('all_journals_app.Cell', on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=100, verbose_name='Тип сообщения',
                            default='', choices=(('critical_value', 'Критическое значение'),
                                                 ('comment', 'Замечание')))
    text = models.TextField(verbose_name='Текст сообщения')

    sendee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='messages_sendee')
    addressee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='messages_adressee')

    link = models.URLField(max_length=128, verbose_name='Ссылка на ячейку', default="#")

    @staticmethod
    def add(cell, message, all=False, positions=None, ids=None, plant=None):
        if not all and positions is None and ids is None and plant is None:
            raise ValueError

        recipients = []
        if ids:
            recipients = list()
            for id in ids:
                recipients.extend(Employee.objects.filter(id=id))
        if positions:
            recipients = list()
            for p in positions:
                recipients.extend(Employee.objects.filter(plant=plant, position=p))
        if all:
            recipients = list()
            recipients.extend(Employee.objects.all())

        text = message['text']
        message.pop('text')

        for emp in recipients:
            Message.objects.update_or_create(**message, defaults={'text': text}, addressee=emp, cell=cell)

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

    @staticmethod
    def get_addressees(all=False, positions=None, ids=None, plant=None):
        """Отдает список адресатов"""

        res = []
        if all:
            return Employee.objects.only('user')
        if positions:
            for p in positions:
                emp = Employee.objects.filter(plant=plant, position=p)
                res.extend(emp)
        if ids:
            for id in ids:
                emp = Employee.objects.get(id=id)
                res.append(emp)

        return res
