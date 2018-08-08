import inspect
import random
import json
import csv

from datetime import timedelta
from inspect import ismethod
from itertools import product
from random import randint
from os import walk

from django.db.models import Model
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from e_logs.furnace.fractional_app.models import *
from e_logs.furnace.fractional_app import models as famodels
from e_logs.common.all_journals_app import models as comodels
from e_logs.common.all_journals_app.models import *
from e_logs.common.all_journals_app.management.commands.fields_descriptions_filler import fill_fields_descriptions
from e_logs.common.all_journals_app.management.commands.tables_filler import fill_tables
from e_logs.common.all_journals_app.management.commands.tables_lists_filler import fill_tables_lists
from e_logs.common.all_journals_app.management.commands.fields_filler import fill_fields
from e_logs.core.utils.webutils import parse, translate
from django.utils.translation import gettext as _
from django.db import connection
from e_logs.common.login_app.models import Employee
from e_logs.core.models import Setting

from e_logs.core.utils.deep_dict import deep_dict
from e_logs.core.utils.usersutils import add_user, get_groups
from e_logs.core.utils.webutils import translate

class DatabaseFiller:
    """
    All fill methods names and only they should be like 'fill_*_table'.
    Filling methods will be called in a random order
    """

    def fill_fractional_app(self, n):
        for i in range(n):
            time = timezone.now() - timedelta(hours=2 * i)
            cinder_masses = [
                c + random.uniform(0, 2)
                for c in [1, 2, 4, 7, 8, 6.5, 3, 2.5, 0.5]
            ]
            schieht_masses = [
                s + random.uniform(0, 2)
                for s in [1, 2, 4, 7, 8, 7, 4, 3, 2, 0.5]
            ]
            cinder_sizes = [
                c + random.uniform(0, 2)
                for c in [0.0,2.0,5.0,10.0,20.0,25.0,33.0,44.0,50.0]
            ]
            schieht_sizes = [
                s + random.uniform(0, 2)
                for s in [0.0,2.0,5.0,10.0,20.0,25.0,33.0,44.0,50.0]
            ]

            journal = Journal.objects.get(name="fractional")
            measurement = Measurement.objects.create(
                time = timezone.now(),
                name = "fractional_anal",
                journal=journal
            )
            table = Table.objects.get_or_create(
                journal=journal,
                name='measurements'
            )[0]
            for i, m_value in enumerate(cinder_masses):
                Cell.objects.create(
                    field=Field.objects.get_or_create(
                        name='cinder_mass',
                        table=table
                    )[0],
                    index=i,
                    value=m_value,
                    group=measurement
                )
            for i, m_value in enumerate(cinder_sizes):
                Cell.objects.create(
                    field=Field.objects.get_or_create(
                        name='cinder_size',
                        table=table
                    )[0],
                    index=i,
                    value=m_value,
                    group=measurement
                )
            for i, m_value in enumerate(schieht_masses):
                Cell.objects.create(
                    field=Field.objects.get_or_create(
                        name='schieht_mass',
                        table=table
                    )[0],
                    index=i,
                    value=m_value,
                    group=measurement
                )
            for i, m_value in enumerate(schieht_sizes):
                Cell.objects.create(
                    field=Field.objects.get_or_create(
                        name='schieht_size',
                        table=table
                    )[0],
                    index=i,
                    value=m_value,
                    group=measurement
                )


    def groupsFromCSV(self):
        user_groups = deep_dict()
        with open('names.csv', encoding='utf-8', newline='') as csvfile:
            users_info = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in users_info:
                info = row[0].split(",")
                position_en = translate(info[1].lower()).replace("-", "_") if len(info) > 1 else ''
                if position_en.find("mastera_smenyi") > 0:
                    position_en = "i.o.mastera_smenyi"
                user_groups[position_en] = info[1].lower()
        return user_groups

    def fill_employees(self):
        with open('names.csv', encoding='utf-8', newline='') as csvfile:
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


    def fill_plants(self):
        Plant.objects.bulk_create([
            Plant(
                name="furnace"
            ),
            Plant(
                name="electrolysis"
            ),
            Plant(
                name="leaching"
            ),
        ])


    def create_number_of_shifts(self):

        Setting(
            name='number_of_shifts',
            scope=Plant.objects.get(name='furnace'),
            value='2'
        ).save()

        Setting(
            name='number_of_shifts',
            scope=Plant.objects.get(name='leaching'),
            value='3'
        ).save()

        Setting(
            name='number_of_shifts',
            scope=Plant.objects.get(name='electrolysis'),
            value='4'
        ).save()

        # overriding number of shifts for furnace plant
        Setting(
            name='number_of_shifts',
            scope=Journal.objects.get(
                plant=Plant.objects.get(
                    name='furnace'
                ),
                name='reports_furnace_area'
            ),
            value='3'
        ).save()


    def fill_journals(self):
        """Call after fill_plants"""

        furnace_plant = Plant.objects.get(name='furnace')
        leaching_plant = Plant.objects.get(name='leaching')
        electrolysis_plant = Plant.objects.get(name='electrolysis')

        Journal.objects.bulk_create([
            Journal(
                name='furnace_changed_fraction',
                plant=furnace_plant
            ),
            Journal(
                name='concentrate_report',
                plant=furnace_plant
            ),
            Journal(
                name='technological_tasks',
                plant=furnace_plant
            ),
            Journal(
                name='reports_furnace_area',
                plant=furnace_plant
            ),
            Journal(
                name='furnace_repair',
                plant=furnace_plant,
                type='equipment'
            ),
            Journal(
                name='report_income_outcome_schieht',
                plant=furnace_plant
            ),
            Journal(
                name='metals_compute',
                plant=furnace_plant
            ),
            Journal(
                name='fractional',
                plant=furnace_plant
            ),
            Journal(
                name='masters_report',
                plant=electrolysis_plant
            ),
            Journal(
                name='electrolysis_technical_report_3_degree',
                plant=electrolysis_plant
            ),
            Journal(
                name='electrolysis_technical_report_4_degree',
                plant=electrolysis_plant
            ),
            Journal(
                name='electrolysis_technical_report_12_degree',
                plant=electrolysis_plant
            ),
            Journal(
                name='electrolysis_repair_report_tables',
                plant=electrolysis_plant,
                type='equipment'
            ),
            Journal(
                name='leaching_repair_equipment',
                plant=leaching_plant,
                type='equipment'
            ),
            Journal(
                name='leaching_express_analysis',
                plant=leaching_plant
            ),
        ])

    def fill_tables(self):
        """Call after fill_journals"""
        fill_tables()

    def fill_fields(self):
        """Call after fill_tables"""
        fill_fields()


    def reset_increment_counter(self, table_name):
        print("Resetting increment counter...")
        with connection.cursor() as cursor:
        # for sqlite
        # cursor.execute(f"UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='{table_name}'")

        # for MS SQL server
            cursor.execute(f'DBCC CHECKIDENT({table_name}, RESEED, 0)')

    def create_permissions_and_groups(self):
        superuser = User.objects.create_superuser("inframine", "admin@admin.com", "Singapore2017")
        superuser.save()
        Employee(name="inframine", position="admin", user=superuser).save()

        content_type = ContentType.objects.get_for_model(Cell)
        modify_leaching = Permission(
            name="Modify Leaching Plant",
            codename="modify_leaching",
            content_type=content_type
        )
        modify_leaching.save()
        modify_furnace = Permission(
            name="Modify Furnace Plant",
            codename="modify_furnace",
            content_type=content_type
        )
        modify_furnace.save()
        modify_electrolysis= Permission(
            name="Modify Electrolysis Plant",
            codename="modify_electrolysis",
            content_type=content_type
        )
        modify_electrolysis.save()

        # Cell permissions
        validate_cells = Permission(
            name="Validate Cells",
            codename="validate_cells",
            content_type=content_type
        )
        validate_cells.save()

        edit_cells = Permission(
            name="Edit Cells",
            codename="edit_cells",
            content_type=content_type
        )
        edit_cells.save()

        view_cells = Permission(
            name="View Cells",
            codename="view_cells",
            content_type=content_type
        )
        view_cells.save()

        # Groups
        laborants = Group(
            name="Laborant",
        )
        laborants.save()
        laborants.permissions.set([edit_cells])
        laborants.save()

        boss = Group(
            name="Boss",
        )
        boss.save()
        boss.permissions.set([validate_cells])
        boss.save()

        leaching = Group(
            name="Leaching",
        )
        leaching.save()
        leaching.permissions.set([modify_leaching])
        leaching.save()

        furnace = Group(
            name="Furnace",
        )
        furnace.save()
        furnace.permissions.set([modify_furnace])
        furnace.save()

        electrolysis = Group(
            name="Electrolysis",
        )
        electrolysis.save()
        electrolysis.permissions.set([modify_electrolysis])
        electrolysis.save()

    def create_tables_lists(self):
        print('Adding table lists for each journal')
        fill_tables_lists()

    # TODO: create the same for tables?
    def create_journals_verbose_names(self):
        journals_verbose_names = {
            'furnace': {
                'furnace_changed_fraction': 'Рабочий журнал изменения фракции',
                'concentrate_report': 'Журнал рапортов о проделанной работе по складам концентратов',
                'technological_tasks': 'Журнал сменных производственных, тех. заданий',
                'reports_furnace_area': 'Журнал печного участка',
                'furnace_repair': 'Журнал по ремонту',
                'report_income_outcome_schieht': 'Поступление, расходы и остатки Zn концентратов',
                'metals_compute': 'Рассчёт металлов',
                'fractional': 'Ситовой анализ огарка и шихты',
            },
            'electrolysis': {
                'masters_report': 'Журнал рапортов мастеров смен',
                'electrolysis_technical_report_3_degree': 'Технологический журнал электролиза 3-й серии',
                'electrolysis_technical_report_4_degree': 'Технологический журнал электролиза 4-й серии',
                'electrolysis_technical_report_12_degree': 'Технологические журналы электролиза 1-й и 2-й серии',
                'electrolysis_repair_report_tables': 'Журнал по ремонту оборудования',
            },
            'leaching': {
                'leaching_repair_equipment': 'Журнал ремонта',
                'leaching_express_analysis': 'Журнал экспресс анализа',
            }
        }
        for plant_name in journals_verbose_names:
            for journal_name, verbose_name in journals_verbose_names[plant].items():
                Setting.objects.create(
                    name='verbose_name',
                    value=verbose_name,
                    scope=Journal.objects.get(
                        plant=Plant.objects.get(name=plant_name),
                        name=journal_name
                    )
                )

    def create_fields_descriptions(self):
        print('Adding fields info settings...')
        fill_fields_descriptions()

    def clean_database(self):
        exception_models = [User, Model]
        db_models = []
        for name, obj in inspect.getmembers(famodels):
            if inspect.isclass(obj) and issubclass(obj, models.Model) and obj not in exception_models:
                db_models.append(obj)

        db_models.extend([Setting, Employee, CellGroup, Cell, Plant, Group, Permission])

        for u in User.objects.all():  # delete user
            u.delete()

        for t in db_models:
            t.objects.all().delete()
