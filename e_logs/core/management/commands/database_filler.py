import csv
import inspect
import random
from typing import List, Optional

from django.contrib.auth.models import User, Group, Permission
from django.db import connection
from django.db.models import Model

from e_logs.common.all_journals_app.models import *
from e_logs.common.login_app.models import Employee
from e_logs.core.management.commands.fields_descriptions_filler import fill_fields_descriptions
from e_logs.core.management.commands.fields_filler import fill_fields
from e_logs.core.management.commands.tables_filler import fill_tables
from e_logs.core.management.commands.tables_lists_filler import fill_tables_lists
from e_logs.core.models import Setting
from e_logs.core.utils.loggers import stdout_logger, err_logger
from e_logs.core.utils.webutils import translate
from e_logs.furnace.fractional_app import models as famodels


class DatabaseFiller:
    @staticmethod
    def fill_fractional_app(n: int):
        def randomize_array(a) -> List[float]:
            return [c + random.uniform(0, 2) for c in a]

        for i in range(n):
            cinder_masses = randomize_array([1, 2, 4, 7, 8, 6.5, 3, 2.5, 0.5])
            schieht_masses = randomize_array([1, 2, 4, 7, 8, 7, 4, 3, 2, 0.5])
            cinder_sizes = randomize_array([0.0, 2.0, 5.0, 10.0, 20.0, 25.0, 33.0, 44.0, 50.0])
            schieht_sizes = randomize_array([0.0, 2.0, 5.0, 10.0, 20.0, 25.0, 33.0, 44.0, 50.0])

            journal = Journal.objects.get(name="fractional")
            measurement = Measurement.objects.create(time=timezone.now(), journal=journal)
            table = Table.objects.get_or_create(journal=journal, name='measurements')[0]

            arr_name_pairs = [(cinder_masses, 'cinder_mass'), (cinder_sizes, 'cinder_size'),
                              (schieht_masses, 'schieht_mass'), (schieht_sizes, 'schieht_size')]

            for arr, name in arr_name_pairs:
                for j, m_value in enumerate(arr):
                    field = Field.objects.get_or_create(name=name, table=table)[0]
                    Cell.objects.create(field=field, index=j, value=round(m_value, 2),
                                        group=measurement)

    @staticmethod
    def _get_groups(position: str, plant: str) -> List[str]:
        groups = []
        if position == " просмотра\"":
            groups.append("Laborant")
        else:
            groups.append("Boss")
        if plant == "ОЦ":
            groups.append("Furnace")
        elif plant == "ЦВЦО":
            groups.append("Leaching")
        else:
            groups.append("Electrolysis")
        return groups

    @staticmethod
    def fill_employees():
        with open('resources/data/names.csv', encoding='utf-8', newline='') as csvfile:
            users_info = csv.reader(csvfile, delimiter=';', quotechar='|')

            for row in users_info:
                info = row[0].split(",")
                user_fio = info[0]
                plant = info[-1]
                position = info[3]
                user_ru = user_fio.split()
                user_en = translate(user_fio).split("-")
                groups = DatabaseFiller._get_groups(position, plant)
                user = {
                    'ru': {
                        'last_name': user_ru[0],
                        'first_name': user_ru[1] if len(user_ru) > 1 else '',
                        'second_name': user_ru[2] if len(user_ru) > 2 else '',
                    },
                    'en': {
                        'last_name': user_en[0],
                        'first_name': user_en[1][0] if len(user_en) > 1 and len(
                            user_en[1]) > 0 else '',
                        'second_name': user_en[2][0] if len(user_en) > 2 and len(
                            user_en[2]) > 0 else ''
                    },
                    'groups': groups
                }
                DatabaseFiller.add_user(user)

    @staticmethod
    def fill_plants():
        plant_names = ['furnace', 'electrolysis', 'leaching']
        Plant.objects.bulk_create([Plant(name=n) for n in plant_names])

    @staticmethod
    def create_number_of_shifts():
        shift_numbers = {'furnace': '2', 'leaching': '3', 'electrolysis': '4'}

        for pl, num in shift_numbers.items():
            plant = Plant.objects.get(name=pl)
            Setting.set_value('number_of_shifts', num, scope=plant)

        # overriding number of shifts for furnace plant
        reports_furn = Journal.objects.get(plant__name='furnace', name='reports_furnace_area')
        Setting.set_value('number_of_shifts', '3', reports_furn)

    @staticmethod
    def add_user(user_dict: dict) -> Optional[User]:
        user_name = (user_dict['en']['last_name']
                     + "-" + user_dict['en']['first_name']
                     + "-" + user_dict['en']['second_name']).strip('-')

        if User.objects.filter(username=user_name).exists():
            err_logger.warning(f'user `{user_name}` already exists')
            return None
        else:
            user = User.objects.create_user(user_name, password='qwerty')
            user.first_name = user_dict['ru']['first_name']
            user.last_name = user_dict['ru']['last_name']
            user.is_superuser = False
            user.is_staff = True
            for group in user_dict["groups"]:
                user.groups.add(Group.objects.get(name=group))
            user.user_permissions.add(Permission.objects.get(codename="view_cells"))

            e = Employee()
            e.name = user.first_name + ' ' + user.last_name
            e.position = user_dict["groups"][0].lower()
            e.plant = user_dict["groups"][1].lower()
            e.user = user

            e.save()

            user.save()
            return user

    @staticmethod
    def fill_journals():
        """Call after fill_plants"""

        plant_to_journal = {
            'furnace': ['furnace_changed_fraction', 'concentrate_report', 'technological_tasks',
                        'reports_furnace_area', 'furnace_repair',
                        'report_income_outcome_schieht', 'metals_compute', 'fractional'],
            'leaching': ['leaching_repair_equipment', 'leaching_express_analysis'],
            'electrolysis': ['masters_report', 'electrolysis_technical_report_3_degree',
                             'electrolysis_technical_report_4_degree',
                             'electrolysis_technical_report_12_degree',
                             'electrolysis_repair_report_tables']
        }

        journals = []
        for plant_name, journal_names in plant_to_journal.items():
            for name in journal_names:
                plant = Plant.objects.get(name=plant_name)
                journal = Journal(name=name, plant=plant)
                journals.append(journal)

        Journal.objects.bulk_create(journals)

    @staticmethod
    def fill_tables():
        """Call after fill_journals"""
        fill_tables()

    @staticmethod
    def fill_fields():
        """Call after fill_tables"""
        fill_fields()

    @staticmethod
    def reset_increment_counter(table_name):
        stdout_logger.info("Resetting increment counter...")
        with connection.cursor() as cursor:
            # for sqlite
            # cursor.execute(f"UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='{table_name}'")

            # for MS SQL server
            cursor.execute(f'DBCC CHECKIDENT({table_name}, RESEED, 0)')

    @staticmethod
    def create_superuser():
        superuser = User.objects.create_superuser("inframine", "admin@admin.com", "Singapore2017")
        superuser.save()
        Employee(name="inframine", position="admin", user=superuser).save()

    @staticmethod
    def create_permissions_and_groups():

        perm_names = ["Modify Leaching Plant", "Modify Furnace Plant", "Modify Electrolysis Plant",
                      "Validate Cells", "Edit Cells", "View Cells"]
        perm_codenames = ["modify_leaching", "modify_furnace", "modify_electrolysis",
                          "validate_cells", "edit_cells", "view_cells"]
        group_perms = {"Laborant": "edit_cells", "Boss": "validate_cells",
                       "Leaching": "modify_leaching", "Furnace": "modify_furnace",
                       "Electrolysis": "modify_electrolysis"}

        content_type = ContentType.objects.get_for_model(Cell)

        for n, cn in zip(perm_names, perm_codenames):
            perm = Permission(name=n, codename=cn, content_type=content_type)
            perm.save()

        for group_name, perm in group_perms.items():
            gr = Group(name=group_name)
            gr.save()  # for many-to-many to work
            perm_obj = Permission.objects.get(codename=perm)
            gr.permissions.set([perm_obj])
            gr.save()

    @staticmethod
    def create_tables_lists():
        stdout_logger.info('Adding table lists for each journal...')
        fill_tables_lists()

    # TODO: create the same for tables?
    @staticmethod
    def create_journals_verbose_names():
        journals_verbose_names = {
            'furnace': {
                'furnace_changed_fraction': 'Рабочий журнал изменения фракции',
                'concentrate_report': 'Журнал рапортов о проделанной работе по'
                                      ' складам концентратов',
                'technological_tasks': 'Журнал сменных производственных, тех. заданий',
                'reports_furnace_area': 'Журнал печного участка',
                'furnace_repair': 'Журнал по ремонту',
                'report_income_outcome_schieht': 'Поступление, расходы и остатки Zn концентратов',
                'metals_compute': 'Рассчёт металлов',
                'fractional': 'Ситовой анализ огарка и шихты',
            },
            'electrolysis': {
                'masters_report': 'Журнал рапортов мастеров смен',
                'electrolysis_technical_report_3_degree':
                    'Технологический журнал электролиза 3-й серии',
                'electrolysis_technical_report_4_degree':
                    'Технологический журнал электролиза 4-й серии',
                'electrolysis_technical_report_12_degree':
                    'Технологические журналы электролиза 1-й и 2-й серии',
                'electrolysis_repair_report_tables': 'Журнал по ремонту оборудования',
            },
            'leaching': {
                'leaching_repair_equipment': 'Журнал ремонта',
                'leaching_express_analysis': 'Журнал экспресс анализа',
            }
        }
        for plant_name in journals_verbose_names:
            for journal_name, verbose_name in journals_verbose_names[plant_name].items():
                Setting.objects.create(name='verbose_name', value=verbose_name,
                                       scope=Journal.objects.get(
                                           plant=Plant.objects.get(name=plant_name),
                                           name=journal_name))

    @staticmethod
    def create_fields_descriptions():
        stdout_logger.info('Adding fields info settings...')
        fill_fields_descriptions()

    @staticmethod
    def load_settings():
        Setting["unfilled_cell"] = ""

    @staticmethod
    def clean_database():
        """
        Deletes all database models
        :return: None
        """
        exception_models = [User, Model]
        db_models = []

        for name, obj in inspect.getmembers(famodels):
            if inspect.isclass(obj) and issubclass(obj, models.Model) \
                    and obj not in exception_models:
                db_models.append(obj)

        db_models.extend([Permission, Setting, Employee, CellGroup, Cell, Plant, Group])

        for u in User.objects.all():  # delete user
            u.delete()

        for t in db_models:
            t.objects.all().delete()
