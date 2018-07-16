from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import csv

from utils.webutils import translate


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument(
            '--default',
            action="store_true",
            help='Default argument',
        )

    def handle(self, *args, **options):
        with open('names.csv', newline='') as csvfile:
            users_info = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in users_info:
                user_fio = row[0].split(",", 1)[0]
                fio_ru_tuple = user_fio.split()
                translated_user_name = translate(user_fio)
                translated_user_name_tuple = translated_user_name.split("-")
                user_dict = {
                    'ru': {
                        'last_name': fio_ru_tuple[0],
                        'first_name': fio_ru_tuple[1] if 1 < len(fio_ru_tuple) else '',
                        'second_name': fio_ru_tuple[2] if 2 < len(fio_ru_tuple) else '',
                    },
                    'en': {
                        'last_name': translated_user_name_tuple[0],
                        'first_name': translated_user_name_tuple[1] if 1 < len(translated_user_name_tuple) else '',
                        'second_name': translated_user_name_tuple[2] if 2 < len(translated_user_name_tuple) else ''
                    }
                }
                user_name = user_dict['en']['last_name'] \
                            + "-" + user_dict['en']['first_name'] \
                            + "-" + user_dict['en']['second_name']
                user = User.objects.create_user(user_name, password='qwerty')
                user.first_name = user_dict['ru']['first_name']
                user.last_name = user_dict['ru']['last_name']
                user.is_superuser = False
                user.is_staff = True
                user.save()

