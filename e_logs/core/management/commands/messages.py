from django.core.management.base import BaseCommand

from e_logs.common.login_app.models import Employee
from e_logs.common.messages_app.models import Message


class Command(BaseCommand):
    help = 'Adding demo messages'

    def handle(self, *args, **options):

        msg = Message(is_read=False,
                      type='critical_value',
                      text='Some text',
                      sendee=Employee.objects.get(name='inframine'),
                      addressee=Employee.objects.get(name='inframine')
                      )
        msg.save()
        # Message.add(cell=None, message={'text': "alfa lorem"}, all_users=True)
        # Message.add(cell=None, message={'text': "betta weryfdgd fdfg fd"}, all_users=True)
        # Message.add(cell=None, message={'text': "gamma iouyew fdgd4r534r dfd g"}, all_users=True)


