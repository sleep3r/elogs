import inspect
import random
import json

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


class DatabaseFiller:
    """
    All fill methods names and only they should be like 'fill_*_table'.
    Filling methods will be called in a random order
    """

    def fill_fractional_app(self, n):
        for i in range(n):
            time = timezone.now() - timedelta(hours=2 * i)
            cinder_masses = [c + random.uniform(0, 2) for c in [1, 2, 4, 7, 8, 6.5, 3, 2.5, 0.5]]
            schieht_masses = [s + random.uniform(0, 2) for s in [1, 2, 4, 7, 8, 7, 4, 3, 2, 0.5]]

            cinder_sizes = [c + random.uniform(0, 2) for c in [0.0,2.0,5.0,10.0,20.0,25.0,33.0,44.0,50.0]]
            schieht_sizes = [s + random.uniform(0, 2) for s in [0.0,2.0,5.0,10.0,20.0,25.0,33.0,44.0,50.0]]

            measurement = Measurement.objects.create(type="measurement", time = timezone.now(), name = "fractional_anal", plant=Plant.objects.get(name="furnace"))

            for i, m_value in enumerate(cinder_masses):
                Cell.objects.create(table_name="measurements", field_name='cinder_mass',
                                index=i, value=m_value, group=measurement)
            for i, m_value in enumerate(cinder_sizes):
                Cell.objects.create(table_name="measurements", field_name='cinder_size',
                                index=i, value=m_value, group=measurement)
            for i, m_value in enumerate(schieht_masses):
                Cell.objects.create(table_name="measurements", field_name='schieht_mass',
                                index=i, value=m_value, group=measurement)
            for i, m_value in enumerate(schieht_sizes):
                Cell.objects.create(table_name="measurements", field_name='schieht_size',
                                index=i, value=m_value, group=measurement)



    # def fill_equipement(self):
    #     eq_list = [
    #         'Агитатор «Манн» №1',
    #         'Агитатор «Манн» №2',
    #         'Агитатор «Манн» №3',
    #         'Сгуститель №1',
    #         'Сгуститель №2',
    #         'Сгуститель №3',
    #         'Питатель ленточный В – 500 мм',
    #         'Элеватор ЦГ-400 №1',
    #         'Элеватор ЦГ-400 №2',
    #         'Транспортер ленточный В – 650 мм',
    #     ]

    #     for e in eq_list:
    #         Equipment(name=e).save()

    # def fill_table_from_journal_page(self, journal_page, table_name, data, do_index=True):
    #     for field_name, values in data.items():
    #         if type(values) is not list:
    #             values = [values]
    #
    #         for i, value in enumerate(values):
    #             index_marker_in_field_name = ""
    #             if type(value) is not str:
    #                 value = str(value)
    #             index = i
    #             Cell(
    #                 journal_page=journal_page,
    #                 table_name=table_name,
    #                 field_name=field_name + index_marker_in_field_name,
    #                 value=value,
    #                 index=index
    #             ).save()
    #
    # def fill_upper_fields_table_jp(self, journal_page):
    #     table_name = "upper_fields"
    #     data = {
    #         "master": "Лупа",
    #         "senior_crane_operator": "Пупа",
    #         "storage": "12-1",
    #         "crane_operator": "Кто-то",
    #         "sling_operator": "Стив Джобс",
    #         "date": "10.12.12",
    #         "shift": "1-200-800"
    #     }
    #     self.fill_table_from_journal_page(journal_page, table_name, data)
    #
    # def fill_lower_fields_table_jp(self, journal_page):
    #     table_name = "lower_fields"
    #     data = {
    #         "notes": "Nice work!",
    #     }
    #     self.fill_table_from_journal_page(journal_page, table_name, data)
    #
    # def fill_big_table_jp(self, journal_page):
    #     table_name = "big_table"
    #     n = 10
    #     data = {
    #         "wagon_num": [1234] * n,
    #         "conc_num": ["ЗГОК"] * n,
    #         "supply_time": ["11:00"] * n,
    #         "dispatch_time": ["12:00"] * n,
    #         "downtime": ["12:00"] * n,
    #         "recieved_conc": [3] * n,
    #         "recieved_beds": [3] * n,
    #         "recieved_stops": [3] * n,
    #         "recieved_braces": [3] * n,
    #         "passed_with_shift": ["Что-нибудь"] * n
    #     }
    #
    #     self.fill_table_from_journal_page(journal_page, table_name, data, do_index=True)
    #
    # def fill_small_table_jp(self, journal_page):
    #     table_name = "small_table"
    #     n = 10
    #     min, max = 10, 100
    #     data = {
    #         "storage": [1, 2],
    #         "containers_reciept": [randint(min, max), randint(min, max)],
    #         "shipped_empty_num": [randint(min, max), randint(min, max)],
    #         "poured_containers_num": [randint(min, max), randint(min, max)],
    #         "residue_empty_containers1": [randint(min, max), randint(min, max)],
    #         "residue_empty_containers2": [randint(min, max), randint(min, max)],
    #         "residue_defective_containers": [randint(min, max), randint(min, max)],
    #         "residue_braces": [randint(min, max), randint(min, max)],
    #         "residue_beds": [randint(min, max), randint(min, max)],
    #         "residue_stops": [randint(min, max), randint(min, max)]
    #     }
    #
    #     self.fill_table_from_journal_page(journal_page, table_name, data)
    #
    #     new_data = dict()
    #     for key in data.keys():
    #         new_data[key + "_total"] = sum(data[key])
    #     new_data["storage_total"] = "Итого"
    #
    #     self.fill_table_from_journal_page(journal_page, table_name, new_data)



    # --------------------------------------------------------------------------------------------
    def fill_employees(self):
        kz_names = ['Абдулкафар', 'Асмет', 'Жолдас', 'Кобжан', 'Суйинбай']
        kz_l_names = ['Ахметов', 'Омаров', 'Оспанов', 'Сулейменов', 'Искаков']
        ru_names = ['Иван', 'Петр', 'Александр', 'Алексей', 'Сергей', 'Василий']
        ru_l_names = ['Иванов', 'Петров', 'Сидоров', 'Пупкин']

        for f, l in product(kz_names, kz_l_names):
            e = Employee()
            e.name = f + ' ' + l
            e.position = 'laborant'
            e.plant = 'electrolysis'
            lname = translate(e.name).replace(' ', '_')
            e.user = User.objects.create_user(lname, lname + '@kazzink.kz', lname)
            e.save()
        for f, l in product(ru_names, ru_l_names):
            e = Employee()
            e.name = f + ' ' + l
            e.position = 'master'
            e.plant = 'furnace'
            lname = translate(e.name).replace(' ', '_')
            e.user = User.objects.create_user(lname, lname + '@kazzink.kz', lname)
            e.save()
        for f, l in product(kz_names, ru_l_names):
            e = Employee()
            e.name = f + ' ' + l
            e.position = 'boss'
            e.plant = 'furnace'
            lname = translate(e.name).replace(' ', '_')
            e.user = User.objects.create_user(lname, lname + '@kazzink.kz', lname)
            e.save()
        for f, l in product(ru_names, kz_l_names):
            e = Employee()
            e.name = f + ' ' + l
            e.position = 'boss'
            e.plant = 'electrolysis'
            lname = translate(e.name).replace(' ', '_')
            e.user = User.objects.create_user(lname, lname + '@kazzink.kz', lname)
            e.save()
        for e in Employee.objects.all():
            if e.position == "boss":
                e.user.groups.add(Group.objects.get(name="Boss"))
            else:
                e.user.groups.add(Group.objects.get(name="Laborant"))

            e.user.groups.add(Group.objects.get(name=e.plant.title()))
            e.user.user_permissions.add(Permission.objects.get(codename="view_cells"))
            e.save()

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

    def fill_journalpages_data(self, journal_page):
        for name in dir(self):
            attribute = getattr(self, name)
            if ismethod(attribute) and name.startswith('fill_') and name.endswith('_table_jp'):
                attribute(journal_page=journal_page)

    def reset_increment_counter(self, table_name):
        print("reset increment counter")
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
        print('Creating table lists for each journal')
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

    # def create_demo_database(self, n):
    #     self.create_permissions_and_groups()
    #     self.fill_plants()
    #     self.fill_employees()
    #     self.fill_fractional_app(n)
    #
    # def recreate_database(self, *args, **kwargs):
    #     self.clean_database()
    #     self.create_demo_databas()
