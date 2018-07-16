from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import csv

from utils.usersutils import add_user
from utils.webutils import translate


class Command(BaseCommand):
    help = 'Adding users from csv file'

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         '--default',
    #         action="store_true",
    #         help='Default argument',
    #     )

    def handle(self, *args, **options):
        with open('names.csv', newline='') as csvfile:
            users_info = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in users_info:
                user_fio = row[0].split(",", 1)[0]
                user_ru = user_fio.split()
                user_en = translate(user_fio).split("-")
                user = {
                    'ru': {
                        'last_name': user_ru[0],
                        'first_name': user_ru[1] if 1 < len(user_ru) else '',
                        'second_name': user_ru[2] if 2 < len(user_ru) else '',
                    },
                    'en': {
                        'last_name': user_en[0],
                        'first_name': user_en[1] if 1 < len(user_en) else '',
                        'second_name': user_en[2] if 2 < len(user_en) else ''
                    }
                }

                add_user(user)
        print("Users added")
