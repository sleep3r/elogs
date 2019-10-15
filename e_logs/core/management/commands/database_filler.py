import csv
import inspect
import random
from typing import List, Optional

from django.contrib.auth.models import User, Group, Permission
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule

from e_logs.business_logic.dictionaries.models import EquipmentDict, ConcentrateDict
from e_logs.business_logic.modes.models import Mode, FieldConstraints
from e_logs.core.journals_git import VersionControl
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
                try:
                    password = row[5]
                except:
                    password = ''

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
                    'password': password
                }
                DatabaseFiller.add_user(user)

        user = CustomUser.objects.create_user('шуиншин-г-м', password='8756')
        user.first_name = "Галымбек"
        user.last_name = "Шуиншин"
        user.is_superuser = False
        user.is_staff = True
        user.groups.add(Group.objects.get(name="senior technologist"))
        for group in user.groups.all():
            for perm in group.permissions.all():
                user.user_permissions.add(perm)
        user.save()
        Employee(name="Галымбек Шуиншин", position="senior technologist", user=user).save()

    @staticmethod
    def fill_plants():
        plant_names = {'furnace': "Обжиг", 'electrolysis': "Электролиз", 'leaching': "Выщелачивание"}
        Plant.objects.bulk_create([Plant(name=name, verbose_name=verbose_name)
                                   for name, verbose_name in plant_names.items()])

    @staticmethod
    @logged
    def create_number_of_shifts():
        shift_numbers = {'furnace': 2, 'leaching': 2, 'electrolysis': 2}

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
                        except:
                            pass

    @staticmethod
    def add_user(user_dict: dict) -> Optional[CustomUser]:
        if user_dict["groups"]:
            last_name = user_dict['ru']['last_name']
            first_name = user_dict['ru']['first_name'][0]
            second_name = user_dict['ru']['second_name'][0] if user_dict['ru']['second_name'] else ''
            user_name = (last_name + '-' + first_name + '-' + second_name).strip('-').lower()

            if CustomUser.objects.filter(username=user_name).exists():
                err_logger.warning(f'user `{user_name}` already exists')
                return None
            else:
                user = CustomUser.objects.create_user(user_name, password=user_dict['password'] or 'qwerty')
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

                groups = [group.name for group in user.groups.all()]

                if 'electrolysis' and 'technologist' in groups:
                    user.user_permissions.add(Permission.objects.get(codename='edit_cells'))

                e = Employee()
                e.name = user.first_name + ' ' + user.last_name
                e.position = user_dict["groups"][0].lower()
                e.plant = user_dict["groups"][1].lower()
                e.user = user

                e.save()

                user.save()
                return user

    @staticmethod
    def create_groups():

        def date_range(start_date, end_date):
            for n in range(int((end_date - start_date).days)):
                yield start_date + timedelta(n)

        now_date = current_date()
        git = VersionControl()
        for journal in Journal.objects.all():
            if journal.type == 'shift':
                number_of_shifts = Shift.get_number_of_shifts(journal)
                for shift_date in date_range(now_date - timedelta(days=7), now_date + timedelta(days=7)):
                    for shift_order in range(1, number_of_shifts + 1):
                        shift, created = Shift.objects.get_or_create(journal=journal, order=shift_order,
                                                                     date=shift_date)
                        shift.version = git.version_of(shift)
                        shift.save()
            elif journal.type == 'year':
                for year in range(2017, current_date().year + 4):
                    year, created = Year.objects.get_or_create(year_date=year, journal=journal)
                    year.version = git.version_of(year)
                    year.save()

            elif journal.type == 'month':
                for year in range(2017, current_date().year + 4):
                    for ind, month in enumerate(['Январь', 'Февраль', 'Март', 'Апрель',
                                                 'Май', 'Июнь', 'Июль', 'Август',
                                                 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'], 1):
                        month, created = Month.objects.get_or_create(year_date=year, month_date=month,
                                                                     month_order=ind,
                                                                     journal=journal)
                        month.version = git.version_of(month)
                        month.save()

            elif journal.type == 'equipment':
                for equipment in EquipmentDict.objects.filter(plant=journal.plant):
                    Equipment.objects.get_or_create(name=equipment.name, journal=journal)

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

        superuser = CustomUser.objects.create_superuser("trofimov", "sergei.v.trofimov@gmail.com", "Singapore2018")
        superuser.save()
        Employee(name="trofimov", position="admin", user=superuser).save()

    @staticmethod
    def create_permissions_and_groups():

        perm_names = ["Modify Leaching Plant", "Modify Furnace Plant", "Modify Electrolysis Plant",
                      "Validate Cells", "Edit Cells", "View Cells"]
        perm_codenames = ["modify_leaching", "modify_furnace", "modify_electrolysis",
                          "validate_cells", "edit_cells", "view_cells"]
        group_perms = {"boss": ("validate_cells", "view_cells"),
                       "leaching": ("modify_leaching",),
                       "furnace": ("modify_furnace",),
                       "electrolysis": ("modify_electrolysis",),
                       "senior technologist": ("modify_leaching", "modify_furnace", "modify_electrolysis",
                                               "validate_cells", "view_cells",),
                       "technologist": ("validate_cells", "view_cells"),
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
                               value=Setting._dumps({"boss": 2, "laborant": 2}))

    @staticmethod
    def fill_dicts():
        equipment = {
            "furnace": ['Грейферные краны', 'Приёмный бункер', 'Ленточный конвейер', 'Измельчитель 1 (дробилка)'
                , 'Измельчитель 2 (дробилка)'
                , 'Наклонный ленточный конвейер (загрузочный)'
                , 'Горизонтальный ленточный конвейер (загрузочный)'
                , 'Печь КС (5 шт)'
                , 'Большой бункер печи «КС» (5 шт)'
                , 'Питатель-весоизмеритель'
                , 'Роторный забрасыватель'
                , 'Малый (вспомогательный) бункер печи «КС» (5 шт)'
                , 'Конвейер ленточный («малый» питатель печи «КС») (5 шт)'
                , 'Форкамера'
                , 'Установка испарительного охлаждения печи'
                , 'Барабан сепаратор УИО печи'
                , 'Подовый шнек печи'
                , 'Аэрохолодильник печи'
                , 'Циклон 1-й ступени, НИОГАЗ-ЦН-15, 2шт'
                , 'Циклон 2-й ступенни, НИОГАЗ-ЦН-15, 2шт'
                , 'Групповые циклоны ЦН-15 (2 шт.)'
                , 'Колокольный затвор коллектора "грязного" газа - 2 шт.'
                , 'Конвейер с погруженными скребками КПС-500 №1'
                , 'Конвейер с погруженными скребками КПС-500 №2'
                , 'Конвейер с погруженными скребками КПС-500 №3'
                , 'Шнек выгрузки печи «КС» на КПС (5 шт)'
                , 'Дымосос левый печи ДН17НЖ (левого вращения)'
                , 'Дымосос правой печи ДН17НЖ (правого вращения)'
                , 'Коллектор «грязного газа»'
                , 'Шнек №1 системы пылеудаления коллектора "грязного" газа'
                , 'Шнек №1 системы пылеудаления коллектора "грязного" газа'
                , 'Колокольный затвор коллектора "грязного" газа - 4 шт.'
                , 'Электрофильтр ГК-60'
                , 'Дымосос правый КС№2 ДС-15НЖ (правое вращение)'
                , 'Дымосос правый КС№2 ДН17НЖ (правое вращение)'
                , 'Подстанция электрофильтр ГК-60'
                , 'Колокольный затвор коллектора «чистого газа»'
                , 'Коллектор «чистого газа»'
                , 'Бак для мазута'
                , 'Нагнетатели 325-11м-1 3шт.'
                , 'Нагнетатель  №1 0-325-11'
                , 'Винтовой маслозаполненный воздушный компресссор Atlas Copco GA 18 VSD FF'
                , 'Насос для подпитки УИО ЦНСГ-60/264 3шт.'
                , 'Элеватор ковшевой сч ЦГ-400 №3'
                , 'Элеватор ковшевой ЦГ-400 №4'
                , 'Вакуум насос (насос ВВН2-50) 2 шт.'
                , 'Циклоны 1-й и 2-й ступени (по 2 шт.) ЦН-15 4 шт.'
                , 'Шнек из-под циклонов'
                , 'Распределительный шнек на аэросепараторы №1 и №2'
                , 'Аэросепараторы 327-45-56 №1 и №2 (2 шт.)'
                , 'Мельница шаровая СМ-6004 № 2'
                , 'Бункер над шаровой мельницей №1'
                , 'Мельница шаровая см-6004А № 1'
                , 'Шнек с мельницы №1 на элеваторы 1,2'
                , 'Элеваторы ковшевой ЦГ-400 №1 и №2 (2 шт.)'
                , 'Шнеки №1 и №2 с элеваторов №1,2'
                , 'Распределительный шнек на аэросепаратор №3'
                , 'Аэросепаратор 327-45-56 №3'
                , 'Бункер над шаровой мельницей №3'
                , 'Мельница шаровая СМ-6004А №3'
                , 'Огарочный транспортер (конвейер ленточный)'
                , 'Шнеки №1 и № 2 из-под аэросепаратора №3 (2 шт.)'
                , 'Шнеки №1 и № 2 из-под аэросепаратора №1 (2 шт.)'
                , 'Шнеки №1 и № 2 из-под аэросепаратора №2 (2 шт.)'
                , 'Шнек с элеватора №1 на КПС-500Т'
                , 'КПС-500Т (конвейер с погруженными скребками) на силоса'
                , 'Силос для накопления огарка'
                , 'Приёмные бункера цеха выщелачивания цинкового огарка'
                , 'Шнек для сброса в свои бункера "над ситом"'
                , 'Бункер огарка №4'
                , 'Бункер огарка №6'
                , 'Бункер огарка №5'
                , 'Бункер огарка №3'
                , 'Бункер огарка №7'
                , 'Нагнетатель №1 0-325-11'],
            "electrolysis": ['Напорный стеклопластиковый  желоб'
                , 'Центральный сливной желоб'
                , 'Баки сборники'
                , 'Коллекторы сборники отработанного электролита'
                , 'Градирни нейтрального электролита'
                , 'Градирни отработанного электролита'
                , 'Кристаллизатор'
                , 'Бак отработанного электролита'
                , 'Баки горячего нейтрального электролита (баки ЦВЦО)'
                , 'Баки холодного нейтрального электролита'
                , 'Насосы для откачки отработанного электролита в бак отработанного раствора и в ЦВЦО'
                , 'Насосы для перекачки электролита на градирни'
                , 'Насосы подачи нейтрального раствора на 3 и 4 серии'
                , 'Пробоотборник нейтрального электролита'
                , 'Пробоотборник отработанного электролита'
                , 'Пробоотборник смешанного электроли'
                , 'Атмосферные градирни отработанного электролита'
                , 'Баки нейтрального электролита'
                , 'Смеситель'
                , 'Напорный стеклопластиковый желоб'
                , 'Электролизные ванны'
                , 'Коллектор сбора отработанного электролита'
                , 'Насосы для откачки растворов'
                , 'Шламовые насосы'
                , 'Шламовый бак'
                , 'Сдирочные столы'
                , 'Бак добавки'
                , 'Бак добавки'
                , 'Катодоочистительная машина'
                , 'Пробоотборник отработанного электролита'
                , 'Пробоотборник смешанного электролита'
                , 'Баки охлажденного электролита'
                , 'Испарители ВИУ'
                , 'Магистраль сброса воды с конденсаторов ВИУ'
                , 'Магистраль охлажденного электролита'
                , 'Напорный стеклопластиковый желоб смешанного электролита'
                , 'Распределительные желоба'
                , 'Желоб отработанного электролита под ванной'
                , 'Барометрический бак'
                , 'Коллектор отработанного электролита'
                , '1 Желоб поступающего нейтрал.  электролита'
                , '1 Магистраль от бака отраб. электролита'
                , 'Чан нейтрального раствора (баки ЦВЦО)'
                , 'Чан отработанного электролита (баки ЦВЦО)'
                , 'Насосы охлажденного электролита'
                , 'Насосы нейтрального раствора'
                , 'Бак отработанного электролита'
                , 'Шламовый бак'
                , 'Бак горячего электролита'
                , 'Насосы перекачки шлама'
                , 'Насосы перекачки отработанного электролита'
                , 'Насосы перекачки отработанного электролита'
                , 'Желоб подачи отработанного электролита в баки ВИУ'
                , 'Пробоотборник отработанного электролита'
                , 'Пробоотборник нейтрального электролита'
                , 'Катодоплавильная печь ИЦК-40'
                , 'Индукционные трансформаторы печи'
                , 'Разливочная карусель Котова'
                , 'Штабелеукладчик '
                , 'Электрокалорифер'
                , 'Изложницы для разлива блоков цинка'
                , 'Электронные весы ОТК'
                , 'Весы“Геркулес”'
                , 'Весы эл. М8100-5ТС5С-12-С'
                , 'Весы «Mettler Toledo» –МЕ-3000'
                , 'Обвязочная машина «Циклоп» по ТУ'
                , 'обзочная машина «Фромм» по ТУ обвязочная лента'
                , 'Рукавный фильтр ФРИК-235'
                , 'Пладь фильтрации 235 м2'
                , 'Рукавный фильтр РФГ-УМС-6'
                , 'Пладь фильтрации 336 м2'
                , 'Дымосос ДН-15'
                , 'Дроссовая установка'
                , 'Приемный бункер'
                , 'Грохот'
                , 'Шнек'
                , 'Элеватор'
                , 'Шнек'
                , 'Бункер накопитель'
                , 'Дымосос ДН-13,5'
                , 'Установка по переработке цинковых и цинк – алюминиевых дроссов УК МК и РЦЗ'
                , 'Опрокидыватель контейнеров'
                , 'Приёмный бункер'
                , 'Питатель - дозатор'
                , 'Ленточный транспортер'
                , 'Элеватор цепной'
                , 'Вибрационный грохот ГИС-31'
                , 'Вибрационный грохот ГИЛ-11'
                , 'Вибрационная мельница'
                , 'Бункер - накопитель'
                , 'Бункер - накопитель'
                , 'Кран - балка'],
            "leaching": ['Транспортёр ленточный B-650мм'
                , 'Шнековый питатель дозатор ДШ 16-5 (2 шт.)'
                , 'Шнековый питатель дозатор ДШ 02-2'
                , 'Элеватор ЦГ-400 (2 шт.)'
                , 'Вагон-весы'
                , 'Агитаторы нейтрального выщелачивания'
                , 'Напорный бак магнофлока'
                , 'Сгустители нейтрального выщелачивания'
                , 'Промывочные сгустители (3 шт.)'
                , 'Теплообменники «Альфа-Лаваль»'
                , 'Агитаторы Аг-М9 (Аг-М10) (2 шт.) – их нет'
                , 'Агитаторы медно-кадмиевой очистки (12 шт.) – одинаковые на всех этапах очистки'
                , 'Сгуститель № 13 медно-кадмиевой очистки'
                , 'Фильтр-пресс «Дифенбах» (11 шт.)'
                , 'Фильтр-пресс «Ларокс» (4 шт.)'
                , 'Агитаторы выщелачивания кадмиевой установки'
                , 'Фильтр-пресс рамный (ручной) (5 шт.)'
                , 'Насос Sulzer WPP 33-100'
                , 'Насос АХ200-150-400 (ЮЖУРАЛГИДРОМАШ)'
                , 'Шаровая мельница'
                , 'Баки напорные'
                , 'Баки нейтрального электролита'
                , 'Баки отработанного электролита'
                , 'Бак растворения железной стружки'
                , 'Насос КНЗ6-30'
                , 'Насос КНЗ8-32'
                , 'Нейтральные чаны 3, 4, 4А, 5'
                , 'Питатель ленточный типа 4488 ДН-У'
                , 'Чаны отработанного электролита 2, 3'
                , 'Чан отработанного электролита 9'
                , 'Агитаторы Аг-13, Аг-14'
                , 'Агитаторы Аг-15 – Аг-22'
                , 'Бак-сборник №20'
                , 'Площадь фильтр-прессов 17-18'
                , 'Площадь рамных фильтр-прессов 15-16 (13-14)'
                , 'Бак для медной пульпы ЦВОЦ'
                , 'Мешалка оборотного кека 1'
                , 'Бак-сборник бедно-кадмиевого раствора'
                , 'Бункер после Сг-13'
                , 'Бак НСПС (нижний слив промывочных сгустителей)'
                , 'Баки ВСПС (верхний слив промывочных сгустителей)'
                , 'Агитаторы Аг-в11 и Аг-в12'
                , 'Бункера ВТВ (высокотемпературного выщелачивания)'
                , 'Бак верхнего слива бункеров ВТВ'
                , 'Бак нижнего слива ВТВ']}

        concentrates = ['Пиритный концентрат',
                        'Цинковый концентрат Усть-Таловка',
                        'Цинковый концентрат Жезкент',
                        'РСР цинковый концентрат',
                        'Цинковый концентрат Шубинский'
                        'Цинковый концентрат шламов Тишинского рудника',
                        'Цинковый концентрат Жайремский месторождение Западное',
                        'Цинковый концентрат на РМК',
                        'Цинковый концентрат Белоусовка']

        for plant_name in equipment:
            for eq in equipment[plant_name]:
                EquipmentDict.objects.create(name=eq, plant=Plant.objects.get(name=plant_name))

        for concentrate in concentrates:
            ConcentrateDict.objects.create(name=concentrate)

    @staticmethod
    def tasks_create():
        per_day_schedule, _ = IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.DAYS
        )
        per_hour_schedule, _ = IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.HOURS
        )
        shift_end_schedule, _ = CrontabSchedule.objects.get_or_create(
            minute='59',
            hour='1,7,13,15,19,23',
        )
        every_year_schedule, _ = CrontabSchedule.objects.get_or_create(
            minute='0',
            hour='0',
            day_of_week='*',
            day_of_month='1',
            month_of_year='*',
        )

        PeriodicTask.objects.create(
            interval=per_day_schedule,
            name='Creating shifts',
            task='e_logs.common.all_journals_app.tasks.create_shifts',
        )
        PeriodicTask.objects.create(
            interval=per_day_schedule,
            name='DB dump',
            task='e_logs.common.all_journals_app.tasks.dump_db',
        )
        PeriodicTask.objects.create(
            crontab=shift_end_schedule,
            name='Check blank shifts',
            task='e_logs.common.all_journals_app.tasks.check_blank_shift',
        )
        PeriodicTask.objects.create(
            crontab=every_year_schedule,
            name='Create month and year groups',
            task='e_logs.common.all_journals_app.tasks.create_moths_and_years',
        )

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
                                         'udel': 'Удельная производительность печей',
                                         'area_class_cinder': 'Участок классификаци огарка',
                                         'electrofilter': 'Участок электрофильтров',
                                         'warehouse_concentrates': 'Склад концентратов',
                                         'airmachines': 'Участок воздуходувных машин',
                                         'fences': 'Ограждения',
                                         'concentration_by_time': 'Концентрация по времени',
                                         'places_of_sampling': 'Места отбора пробы',
                                         'corrective_actions': 'Корректирующие действия',
                                         'self_protection': 'Самоохрана', 'worth': 'Мат. Тех. Ценности'},
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
                cell, created = Cell.get_or_create_cell(group_id=group_id, table_name=table_name,
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
                cell, created = Cell.get_or_create_cell(group_id=group_id, table_name=table_name,
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
