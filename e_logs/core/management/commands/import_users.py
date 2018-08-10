from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from management.commands.database_filler import DatabaseFiller


class Command(BaseCommand):
    help = 'Adding users from csv file'

    @staticmethod
    def add_user_to_group(user, group_name):
        group = Group.objects.get(name=f'{group_name}')
        user.groups.add(group)

    def handle(self, *args, **options):
        DatabaseFiller.fill_employees()
