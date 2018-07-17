from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import csv

from utils.usersutils import add_user
from utils.webutils import translate


class Command(BaseCommand):
    help = 'Adding users from csv file'

    def handle(self, *args, **options):
        with open('names.csv', newline='') as csvfile:
            users_info = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in users_info:
                info = row[0].split(",")
                user_fio = info[0]
                print(info)
                user_ru = user_fio.split()
                user_en = translate(user_fio).split("-")
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
                    }
                }

                add_user(user)
        print("Users added")
