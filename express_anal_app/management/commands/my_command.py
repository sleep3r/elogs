from django.core.management.base import BaseCommand


from express_anal_app.tables import command_to_process

class Command(BaseCommand):
    def handle_noargs(self, **options):
        command_to_process()

    def handle(self, *args, **options):
        command_to_process()