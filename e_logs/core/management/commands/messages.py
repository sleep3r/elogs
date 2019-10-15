from django.core.management.base import BaseCommand

from e_logs.common.login_app.models import Employee
from e_logs.common.messages_app.models import Message


class Command(BaseCommand):
    help = 'Adding demo messages'

    def handle(self, *args, **options):

        for i in range(0, 30):
            msg = Message(is_read=False,
                          type='critical_value',
                          text=f'Some text n {i}',
                          sendee=Employee.objects.get(name='inframine'),
                          addressee=Employee.objects.get(name='inframine')
                          )
            msg.save()
