import csv
import inspect
import random
from typing import List, Optional

from django.contrib.auth.models import User, Group, Permission

from e_logs.business_logic.modes.models import Mode, FieldConstraints
from e_logs.core.models import CustomUser
from django.db import connection
from django.db.models import Model
from slugify import slugify

from e_logs.common.all_journals_app.models import *
from e_logs.common.all_journals_app.fields_descriptions.fields_info import fields_info_desc
from e_logs.common.login_app.models import Employee
from e_logs.core.management.commands.fields_descriptions_filler import fill_fields_descriptions
from e_logs.core.management.commands.fields_filler import fill_fields
from e_logs.core.management.commands.tables_filler import fill_tables
from e_logs.core.management.commands.tables_lists_filler import fill_tables_lists
from e_logs.core.models import Setting
from e_logs.core.utils.loggers import stdout_logger, err_logger
from e_logs.core.utils.webutils import logged


class DatabaseFiller:
    @staticmethod
    def _get_groups(position: str, plant: str):
        groups = []
        if position == "начальник цеха":
            groups.append("boss")
        elif position == "технолог цеха":
            groups.append("technologist")
        elif position == "старший мастер":
            groups.append("senior master")
        elif position == "мастер смены":
            groups.append("master")
        elif position == "аппаратчик":
            groups.append("hydro")
        elif position == "мастер цеха":
            groups.append("plant master")
        elif position == "начальник отделения":
            groups.append("department director")
        elif position == "дежурный по электролизу":
            groups.append("electrolysis duty")
        else:
            return None


        if plant == "ОЦ":
            groups.append("furnace")
        elif plant == "ЦВЦО":
            groups.append("leaching")
        elif plant == "ЭЦ":
            groups.append("electrolysis")
        else:
            return None


        return groups

    @staticmethod
    def fill_employees():
        with open('resources/data/names.csv', encoding='utf-8', newline='') as csvfile:
            users_info = csv.reader(csvfile, delimiter=';', quotechar='|')

            for row in users_info:
                fio = row[0]
                user_ru = fio.split()
                user_en = slugify(fio).split("-")
                position = row[1]
                email = row[3]
                plant = row[4]

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
                    'groups': groups,
                    'email': email,
                }
                DatabaseFiller.add_user(user)

        user = CustomUser.objects.create_user('shaukenov-shalkar', password='qwerty')
        user.first_name = "Шалкар"
        user.last_name = "Шаукенов"
        user.is_superuser = False
        user.is_staff = True
        user.groups.add(Group.objects.get(name="senior technologist"))
        for group in user.groups.all():
            for perm in group.permissions.all():
                user.user_permissions.add(perm)
        user.save()
        Employee(name="Шалкар Шаукенов", position="senior technologist", user=user).save()


    @staticmethod
    def fill_plants():
        plant_names = {'furnace':"Обжиг", 'electrolysis':"Электролиз", 'leaching':"Выщелачивание"}
        Plant.objects.bulk_create([Plant(name=name, verbose_name=verbose_name)
                                   for name, verbose_name in plant_names.items()])

    @staticmethod
    @logged
    def create_number_of_shifts():
        shift_numbers = {'furnace': 2, 'leaching': 3, 'electrolysis': 4}

        for pl, num in shift_numbers.items():
            plant = Plant.objects.get(name=pl)
            Setting.of(obj=plant)['number_of_shifts'] = num

        # overriding number of shifts for furnace plant
        reports_furn = Journal.objects.get(plant__name='furnace', name='reports_furnace_area')
        Setting.of(obj=reports_furn)['number_of_shifts'] = 3

    @staticmethod
    def create_modes():
        for plant in Plant.objects.all():
            for journal in Journal.objects.filter(plant=plant).cache():
                for table in Table.objects.filter(journal=journal).cache():
                    for field in Field.objects.filter(table=table).cache():
                        try:
                            desc = fields_info_desc[journal.name][table.name][field.name]
                            if 'min_normal' in desc.keys():
                                mode = Mode.objects.get_or_create(is_active=True,
                                                                  message=f'Основной режим: {journal.verbose_name}',
                                                                  journal=journal)[0]
                                FieldConstraints.objects.create(min_normal=desc.get('min_normal'),
                                                                max_normal=desc.get('max_normal'),
                                                                field=field, mode=mode)
                                print(plant.name, journal.name, table.name, field.name,
                                      desc.get('min_normal', None), desc.get('max_normal', None))
                        except:
                            pass

    @staticmethod
    def add_user(user_dict: dict) -> Optional[CustomUser]:
        if user_dict["groups"]:
            user_name = (user_dict['en']['last_name']
                         + "-" + user_dict['en']['first_name']
                         + "-" + user_dict['en']['second_name']).strip('-')

            if CustomUser.objects.filter(username=user_name).exists():
                err_logger.warning(f'user `{user_name}` already exists')
                return None
            else:
                user = CustomUser.objects.create_user(user_name, password='qwerty')
                user.first_name = user_dict['ru']['first_name']
                user.last_name = user_dict['ru']['last_name']
                user.is_superuser = False
                user.is_staff = False
                user.email = user_dict['email']
                for group in user_dict["groups"]:
                    user.groups.add(Group.objects.get(name=group))
                for group in user.groups.all():
                    for perm in group.permissions.all():
                        user.user_permissions.add(perm)

                e = Employee()
                e.name = user.first_name + ' ' + user.last_name
                e.position = user_dict["groups"][0].lower()
                e.plant = user_dict["groups"][1].lower()
                e.user = user

                e.save()

                user.save()
                return user

    @staticmethod
    def create_shifts():

        def date_range(start_date, end_date):
            for n in range(int((end_date - start_date).days)):
                yield start_date + timedelta(n)

        now_date = current_date()
        for journal in Journal.objects.all():
            if journal.type == 'shift':
                number_of_shifts = Shift.get_number_of_shifts(journal)
                for shift_date in date_range(now_date - timedelta(days=7), now_date + timedelta(days=7)):
                    for shift_order in range(1, number_of_shifts + 1):
                        Shift.objects.get_or_create(journal=journal, order=shift_order,
                                                    date=shift_date)
    @staticmethod
    def fill_journals():
        """Call after fill_plants"""

        plant_to_journal = {
            'furnace': ['furnace_changed_fraction', 'concentrate_report', 'technological_tasks',
                        'reports_furnace_area', 'furnace_repair',
                        'report_income_outcome_schieht', 'metals_compute'],
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
        superuser = CustomUser.objects.create_superuser("inframine", "admin@admin.com", "Singapore2017")
        superuser.save()
        Employee(name="inframine", position="admin", user=superuser).save()

    @staticmethod
    def create_permissions_and_groups():

        perm_names = ["Modify Leaching Plant", "Modify Furnace Plant", "Modify Electrolysis Plant",
                      "Validate Cells", "Edit Cells", "View Cells"]
        perm_codenames = ["modify_leaching", "modify_furnace", "modify_electrolysis",
                          "validate_cells", "edit_cells",  "view_cells"]
        group_perms = {"boss": ("validate_cells", "view_cells"),
                       "leaching": ("modify_leaching",),
                       "furnace": ("modify_furnace",),
                       "electrolysis": ("modify_electrolysis",),
                       "senior technologist":("modify_leaching", "modify_furnace", "modify_electrolysis",
                          "validate_cells", "view_cells",),
                       "technologist":("validate_cells", "view_cells",),
                       "senior master": ("validate_cells", "view_cells", "edit_cells"),
                       "master": ("view_cells", "edit_cells"),
                       "hydro": ("view_cells", "edit_cells"),
                       "plant master": ("validate_cells", "view_cells", "edit_cells"),
                       "department director": ("validate_cells", "view_cells"),
                       "electrolysis duty": ("view_cells", "edit_cells")}

        content_type = ContentType.objects.get_for_model(Cell)

        for n, cn in zip(perm_names, perm_codenames):
            perm = Permission(name=n, codename=cn, content_type=content_type)
            perm.save()

        for group_name, perms in group_perms.items():
            gr = Group(name=group_name)
            gr.save()  # for many-to-many to work
            for perm in perms:
                perm_obj = Permission.objects.get(codename=perm)
                gr.permissions.add(perm_obj)
            gr.save()

    @staticmethod
    def bl_create():
        Setting.objects.create(name='shift_assignment_time',
                               value=Setting._dumps({"hours": 1}))

        Setting.objects.create(name='shift_edition_time',
                               value=Setting._dumps({"hours": 12}))

        Setting.objects.create(name='allowed_positions',
                               value=Setting._dumps({"boss":2, "laborant":2}))

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
                'reports_furnace_area': 'Технологический журнал процесса производства огарка',
                'furnace_repair': 'Журнал по ремонту',
                'report_income_outcome_schieht': 'Поступление, расходы и остатки Zn концентратов',
                'metals_compute': 'Рассчёт металлов',
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
                journal = Journal.objects.get(plant__name=plant_name, name=journal_name)
                journal.verbose_name = verbose_name
                journal.save()


    @staticmethod
    def create_tables_verbose_names():
        tables_verbose_names = {
            'furnace': {
                'furnace_changed_fraction': {'main': 'Изменение фракции'},
                'concentrate_report': {'big': 'Поступление/отгрузка/остаток',
                                       'small': 'Учёт контейнеров', 'upper': 'Состав смены'},
                'technological_tasks': {'main': 'Технологические задания'},
                'reports_furnace_area': {'main': 'Печной участок',
                                         'udel':'Удельная производительность печей',
                                         'area_class_cinder':'Участок классификаци огарка',
                                         'electrofilter':'Участок электрофильтров',
                                         'warehouse_concentrates': 'Склад концентратов',
                                         'airmachines':'Участок воздуходувных машин',
                                         'fences':'Ограждения',
                                         'concentration_by_time':'Концентрация по времени',
                                         'places_of_sampling':'Места отбора пробы',
                                         'corrective_actions':'Корректирующие действия',
                                         'self_protection':'Самоохрана', 'worth':'Мат. Тех. Ценности'},
                'furnace_repair': {'repair': 'Ремонты по Обжиговому цеху'},
                'report_income_outcome_schieht': {'main': '', 'summary': 'НЗП и склады',
                                    'supply_of_zinc_concentrates': 'Поставка цинковых концентратов',
                                    'year_plan_schieht': 'Расчет годового плана шихты'},
                'metals_compute': {'avg_month': 'Среднее содержание за месяц',
                                   'cinder_conc': 'Огарок', 'concentrat': 'Концентрат',
                                   'contain_zn': 'Содержание в', 'gof': 'ГОФ таблица',
                                   'main': 'Среднее содержание за месяц', 'sgok': 'СГОК таблица',
                                   'sns': 'СНС'},
            },
            'electrolysis': {
                'masters_report': {'last': 'Последняя таблица',
                                   'melt_area1': 'Плавильный участок-1',
                                   'melt_area2': 'Плавильный участок-2', 'params': 'Параметры',
                                   'seria1': '1-я 2-я серия', 'seria3': '3-я серия',
                                   'seria4': '4-я серия', 'zinc': 'Цинк товарный'},
                'electrolysis_technical_report_3_degree':
                    {'left': 'Время замеров и работа оборудования',
                     'right': 'Технологический режим, ПАВ и кристаллизаторы'},
                'electrolysis_technical_report_4_degree':
                    {'left': 'Время замеров и работа оборудования',
                     'right': 'Технологический режим, ПАВ и кристаллизаторы'},
                'electrolysis_technical_report_12_degree':
                    {'left': 'Время замеров и работа оборудования',
                     'right': 'Технологический режим, ПАВ и кристаллизаторы'},
                'electrolysis_repair_report_tables': {'main': 'Ремонт'},
            },
            'leaching': {
                'leaching_repair_equipment': {'repair': 'Журнал ремонтов'},
                'leaching_express_analysis': {'agitators': 'Агитаторы очистки',
                                              'appt_hydrometal': 'Аппаратчик - гидрометаллург',
                                              'cinder': 'Огарок', 'loads': 'Нагрузки',
                                              'neutral': 'Нейтральный раствор',
                                              'neutral_thickeners': 'Нейтральные сгуситители',
                                              'reagents': 'Реагенты',
                                              'sample': 'Пробник', 'self_protection': 'Самоохрана',
                                              'shift_info': 'Смена',
                                              'tanks_availability': 'Свободные ёмкости',
                                              'tanks_for_finished_products': 'Баки готовой продукции',
                                              'thickeners': 'Сгустители', 'vsns': 'BCHC',
                                              'zinc_pulp': 'Цинковая пульпа'},
            }
        }

        for plant in tables_verbose_names:
            for journal in tables_verbose_names[plant]:
                for table, table_title in tables_verbose_names[plant][journal].items():
                    t = Table.objects.get(journal__name=journal, name=table)
                    t.verbose_name = table_title
                    t.save()


    @staticmethod
    def create_dashboard_sample_data():
        journal = Journal.objects.get(name="concentrate_report")
        cellgroups = CellGroup.objects.filter(journal=journal)
        shifts = Shift.objects.filter(cellgroup_ptr__in=cellgroups).order_by("date")
        group_ids = shifts[:14].values_list("cellgroup_ptr", flat=True)

        table_name = "small"
        field_names = ["poured_containers_num1", "shipped_empty_num1"]

        for group_id in group_ids:
            for field_name in field_names:
                cell = Cell.get_or_create_cell(group_id=group_id, table_name=table_name,
                    field_name=field_name, index=0)
                cell.value = str(random.randint(0, 100))
                cell.save()

    @staticmethod
    def create_formula_sample_data():
        journal = Journal.objects.get(name="concentrate_report")
        table = Table.objects.get(name="small", journal=journal)
        cellgroups = CellGroup.objects.filter(journal=journal)
        shifts = Shift.objects.filter(cellgroup_ptr__in=cellgroups).order_by("date")
        group_ids = shifts[:14].values_list("cellgroup_ptr", flat=True)

        table_name = "small"
        field_names = ["residue_empty_containers11", "residue_empty_containers21"]
        formula_field_names = ["residue_defective_containers1"]

        for field_name in formula_field_names:
            field = Field.objects.get(name=field_name, table=table)
            field.formula = "FUNC('concentrate_report','small', 'residue_empty_containers11', 0, CURRENT_SHIFT) + FUNC('concentrate_report','small', 'residue_empty_containers21', 0, CURRENT_SHIFT)"
            field.save()
        for group_id in group_ids:
            for field_name in field_names:
                cell = Cell.get_or_create_cell(group_id=group_id, table_name=table_name,
                    field_name=field_name, index=0)
                cell.value = str(random.randint(0, 100))
                cell.save()



    @staticmethod
    def create_fields_descriptions():
        stdout_logger.info('Adding fields info settings...')
        fill_fields_descriptions()


    @staticmethod
    def clean_database():
        """
        Deletes all database models
        :return: None
        """
        exception_models = [CustomUser, Model]
        db_models = []

        db_models.extend([Permission, Setting, Employee, CellGroup, Cell, Plant, Group])

        for u in CustomUser.objects.all():  # delete user
            u.delete()

        for t in db_models:
            t.objects.all().delete()
