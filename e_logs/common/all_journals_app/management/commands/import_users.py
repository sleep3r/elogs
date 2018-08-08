from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
import csv

from e_logs.core.utils.deep_dict import deep_dict
from e_logs.core.utils.usersutils import add_user, get_groups
from e_logs.core.utils.webutils import translate

from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Adding users from csv file'

    @staticmethod
    def add_user_to_group(user, group_name):
        group = Group.objects.get(name=f'{group_name}')
        user.groups.add(group)

    @staticmethod
    def groups_from_csv():
        user_groups = deep_dict()
        with open('resoueces/data/names.csv', encoding='utf-8', newline='') as csvfile:
            users_info = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in users_info:
                info = row[0].split(",")
                position_en = translate(info[1].lower()).replace("-", "_") if len(info) > 1 else ''
                if position_en.find("mastera_smenyi") > 0:
                    position_en = "i.o.mastera_smenyi"
                user_groups[position_en] = info[1].lower()

        return user_groups

    def handle(self, *args, **options):
        with open('resoueces/data/names.csv', encoding='utf-8', newline='') as csvfile:
            users_info = csv.reader(csvfile, delimiter=';', quotechar='|')
            # user_groups = self.groupsFromCSV()
            # add_groups(user_groups)

            for row in users_info:
                info = row[0].split(",")
                user_fio = info[0]
                plant = info[-1]
                position = info[3]
                user_ru = user_fio.split()
                user_en = translate(user_fio).split("-")
                groups = get_groups(position, plant)
                user = {
                    'ru': {
                        'last_name': user_ru[0],
                        'first_name': user_ru[1] if len(user_ru) > 1 else '',
                        'second_name': user_ru[2] if len(user_ru) > 2 else '',
                    },
                    'en': {
                        'last_name': user_en[0],
                        'first_name': user_en[1][0] if len(user_en) > 1 and len(user_en[1]) > 0 else '',
                        'second_name': user_en[2][0] if len(user_en) > 2 and len(user_en[2]) > 0 else ''
                    },
                    'groups': groups
                }
                add_user(user)
