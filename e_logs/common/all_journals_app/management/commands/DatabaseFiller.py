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
    #
    # def fill_denser_anal_table(self, shift):
    #     journal = Journal.objects.get(name='Журнал экспресс анализов')
    #
    #     times = [parse('07.01.2017 10:00:00'), parse('07.01.2017 12:00:00'), parse('07.01.2017 18:00:00')]
    #     sinks = ['ls', 'hs']
    #     points = ['10', '11', '12']
    #
    #     for t, s, p in product(times, sinks, points):
    #         da = DenserAnal(shift=shift, journal=journal, time=t, sink=s, point=p)
    #         for attr in ['ph', 'cu', 'fe', 'liq_sol']:
    #             setattr(da, attr, random.uniform(0, 100))
    #         da.save()
    #
    # def fill_express_anal_table(self, shift):
    #     journal = Journal.objects.get(name='Журнал экспресс анализов')
    #
    #     times = [parse('07.01.2017 10:00:00'), parse('07.01.2017 12:00:00'), parse('07.01.2017 18:00:00')]
    #     points = ['lshs', 'larox', 'purified', 'prod_correction']
    #
    #     for t, p in product(times, points):
    #         lea = LeachingExpressAnal(shift=shift, journal=journal, time=t, point=p)
    #         if p == 'lshs':
    #             for attr in ['co', 'sb', 'cu', 'cu_st1', 'cd', 'solid_st1', 'ph', 'fe', 'arsenic', 'solid', 'density']:
    #                 setattr(lea, attr, random.uniform(0, 100))
    #         elif p == 'larox':
    #             for attr in ['co', 'sb', 'cd', 'solid', 'ph']:
    #                 setattr(lea, attr, random.uniform(0, 100))
    #         elif p == 'purified':
    #             for attr in ['cd', 'co', 'sb', 'cu', 'fe', 'current', 'density', '']:
    #                 setattr(lea, attr, random.uniform(0, 100))
    #         lea.save()
    #
    #         if p == 'prod_correction':
    #             pe = ProductionError(shift=shift, journal=journal, time=t)
    #             for attr in ['norm', 'fact', 'error']:
    #                 setattr(pe, attr, random.uniform(0, 100))
    #
    #             pe.correction = gen_text()
    #             pe.verified = bool(random.randint(0, 1))
    #             pe.save()
    #
    # def fill_solutions_table(self, shift):
    #     journal = Journal.objects.get(name='Журнал экспресс анализов')
    #
    #     times = [parse('07.01.2017 10:00:00'), parse('07.01.2017 12:00:00'), parse('07.01.2017 18:00:00')]
    #
    #     for t in times:
    #         zpa = ZnPulpAnal(shift=shift, journal=journal, time=t)
    #         for attr in ['liq_sol', 'ph', 't0']:
    #             setattr(zpa, attr, random.uniform(0, 100))
    #         zpa.save()
    #
    #         cpa = CuPulpAnal(shift=shift, journal=journal, time=t)
    #         for attr in ['liq_sol', 'before', 'after', 'solid']:
    #             setattr(cpa, attr, random.uniform(0, 100))
    #         cpa.zn_pulp_anal = zpa
    #         cpa.save()
    #
    #         fsa = FeSolutionAnal(shift=shift, journal=journal, time=t)
    #         for attr in ['h2so4', 'solid', 'sb', 'cu', 'fe', 'density', 'arsenic', 'cl']:
    #             setattr(fsa, attr, random.uniform(0, 100))
    #         fsa.zn_pulp_anal = zpa
    #         fsa.cu_pulp_anal = cpa
    #         fsa.save()
    #
    #         da = DailyAnalysis(shift=shift, journal=journal, time=t)
    #         for attr in ['shlippe_sb', 'activ_sas', 'circulation_denser', 'fe_hi1', 'fe_hi2']:
    #             setattr(da, attr, random.uniform(0, 100))
    #         da.save()
    #
    # def fill_hydrometal1_table(self, shift):
    #     journal = Journal.objects.get(name='Журнал экспресс анализов')
    #
    #     times = [parse('07.01.2017 10:00:00'), parse('07.01.2017 12:00:00'), parse('07.01.2017 18:00:00')]
    #
    #     for t in times:
    #         for m in [1, 4]:
    #             attrs = ['ph', 'acid', 'fe2', 'fe_total'] if (m == 1) else ['ph', 'cu', 'fe2', 'sb', 'sediment']
    #             hm = HydroMetal(shift=shift, journal=journal, time=t, mann_num=m)
    #             for attr in attrs:
    #                 setattr(hm, attr, random.uniform(0, 100))
    #             hm.employee = shift.laborant
    #             hm.save()
    #
    #         attrs = ['gran', 'gran_avg', 'fe_avg', 'fe_shave']
    #         cd = CinderDensity(shift=shift, journal=journal, time=t)
    #         for attr in attrs:
    #             setattr(cd, attr, random.uniform(0, 100))
    #         cd.employee = shift.laborant
    #         cd.save()
    #
    # def fill_agitators_table(self, shift):
    #     journal = Journal.objects.get(name='Журнал экспресс анализов')
    #
    #     times = [parse('07.01.2017 10:00:00'), parse('07.01.2017 12:00:00'), parse('07.01.2017 18:00:00')]
    #     nums = [13, 15, 17, 19]
    #
    #     for t, n, b in product(times, nums, (True, False)):
    #         if n == 13:
    #             attrs = ['cd', 'cu', 'co']
    #         elif n == 15:
    #             attrs = ['ph', 'cu']
    #         elif n == 17:
    #             attrs = ['ph', 'cu']
    #         else:
    #             attrs = ['h2so4', 'cu']
    #
    #         aa = Agitators(shift=shift, journal=journal, time=t, num=n, before=b)
    #         for attr in attrs:
    #             setattr(aa, attr, random.uniform(0, 100))
    #
    #         aa.employee = shift.laborant
    #         aa.comment = gen_text()
    #         aa.save()
    #
    # def fill_neutral_table(self, shift):
    #     journal = Journal.objects.get(name='Журнал экспресс анализов')
    #
    #     time = parse('07.01.2017 10:00:00')
    #     nums = [1, 2, 3, 4, 5, 6, 7, 8, 13]
    #
    #     for n in nums:
    #         nd = NeutralDenser(shift=shift, journal=journal, time=time, num=n)
    #         for attr in ['sediment', 'liq_sol1', 'liq_sol2']:
    #             setattr(nd, attr, random.uniform(0, 100))
    #         nd.save()
    #
    # def fill_ready_product_table(self, shift):
    #     journal = Journal.objects.get(name='Журнал экспресс анализов')
    #
    #     time = parse('07.01.2017 10:00:00')
    #     num_fields = ['cd', 'cu', 'co', 'sb', 'fe', 'vt', 'density', 'norm', 'fact']
    #     str_fields = ['correction']
    #     nums = [3, 4, 5]
    #
    #     for n in nums:
    #         rp = ReadyProduct(shift=shift, journal=journal, time=time, num=n)
    #         for attr in num_fields:
    #             setattr(rp, attr, random.uniform(0, 100))
    #         for attr in str_fields:
    #             val = gen_text()
    #             setattr(rp, attr, val)
    #         rp.save()
    #
    # def fill_free_tank_table(self, shift):
    #     journal = Journal.objects.get(name='Журнал экспресс анализов')
    #
    #     nums = range(12)
    #     time = parse('07.01.2017 10:00:00')
    #     num_fields = ['prev_measure', 'cur_measure', 'deviation']
    #     str_fields = ['tank_name']
    #
    #     names = [_('Бак отработ. 1-2 серий'), _('Манны №1-9'), _('Манны ВТВ №10-12'),
    #              _('Обор-й сгуститель №9'), _('Агитатор 22'), _('Бак нейтр. р-ра, 1-й цех'),
    #              _('Ман отраб. № 2, 1-й цех'), _('Ман отраб. № 3, 1-й цех'), _('Ман отраб. № 9, 1-й цех'),
    #              _('-'), _('СМЕННЫЙ БАЛАНС'), _('СУТОЧНЫЙ БАЛАНС')]
    #
    #     for n in nums:
    #         ft = FreeTank(shift=shift, journal=journal, time=time, str_num=n)
    #         for attr in num_fields:
    #             setattr(ft, attr, random.uniform(0, 100))
    #         for attr in str_fields:
    #             val = names[n]
    #             setattr(ft, attr, val)
    #         ft.save()
    #
    # def fill_sample2_table(self, shift):
    #     journal = Journal.objects.get(name='Журнал экспресс анализов')
    #
    #     num_fields = ['cd', 'cu']
    #     times = [parse('07.01.2017 10:00:00'), parse('07.01.2017 12:00:00'),
    #              parse('07.01.2017 14:00:00'), parse('07.01.2017 16:00:00')]
    #
    #     for t in times:
    #         s2 = Sample2(shift=shift, journal=journal, time=t)
    #         for attr in num_fields:
    #             setattr(s2, attr, random.uniform(0, 100))
    #         s2.save()
    #
    # def fill_veu_table(self, shift):
    #     journal = Journal.objects.get(name='Журнал экспресс анализов')
    #
    #     nums = range(3)
    #     num_fields = ['hot', 'cold']
    #     str_fields = ['comment']
    #     time = parse('07.01.2017 10:00:00')
    #
    #     for n in nums:
    #         veu = VEU(shift=shift, journal=journal, time=time, num=n)
    #         for attr in num_fields:
    #             setattr(veu, attr, random.uniform(0, 100))
    #         for attr in str_fields:
    #             val = gen_text()
    #             setattr(veu, attr, val)
    #         veu.save()
    #
    # def fill_neutral_solution_table(self, shift):
    #     journal = Journal.objects.get(name='Журнал экспресс анализов')
    #
    #     nums = range(9)
    #     num_fields = ['value']
    #     str_fields = ['tank_name']
    #     time = parse('07.01.2017 10:00:00')
    #
    #     for n in nums:
    #         ns = NeutralSolution(shift=shift, journal=journal, time=time, str_num=n)
    #         for attr in num_fields:
    #             setattr(ns, attr, random.uniform(0, 100))
    #         for attr in str_fields:
    #             val = gen_text()
    #             setattr(ns, attr, val)
    #         ns.save()
    #
    # def fill_shift_info_table(self, shift):
    #     journal = Journal.objects.get(name='Журнал экспресс анализов')
    #
    #     time = parse('07.01.2017 10:00:00')
    #     num_fields = ['out_sol_t', 'out_sol_c', 'out_pulp_cvck', 'out_cu_kek', 'out_cd_sponge',
    #                   'out_electr', 'out_ruch_cd', 'out_neutr', 'out_cu_pulp', 'in_filtrate_ls', 'in_filtrate_dens',
    #                   'in_fe', 'in_fe_hi', 'in_poor_cd', 'free_13', 'free_14']
    #
    #     si = ShiftInfo(shift=shift, journal=journal, time=time)
    #     for attr in num_fields:
    #         setattr(si, attr, random.uniform(0, 100))
    #
    #     si.this_master = Employee.objects.all()[0]
    #     si.next_master = Employee.objects.all()[1]
    #     si.furnaces = '45'
    #     si.free_13_t = '3'
    #     si.free_14_t = '0ч'
    #
    #     si.save()
    #
    # def fill_self_sequrity_table(self, shift):
    #     journal = Journal.objects.get(name='Журнал экспресс анализов')
    #
    #     times = [parse('07.01.2017 12:00:00'), parse('07.01.2017 14:00:00'), parse('07.01.2017 16:00:00')]
    #     bignote = gen_text(lines=4)
    #
    #     for t in times:
    #         ss = SelfSecurity(shift=shift, journal=journal, time=t)
    #         ss.note = gen_text()
    #         ss.bignote = bignote
    #         ss.save()
    #
    # def fill_scheiht_table(self, shift):
    #     journal = Journal.objects.get(name='Журнал экспресс анализов')
    #
    #     nums = range(3)
    #     time = parse('07.01.2017 10:00:00')
    #
    #     for n in nums:
    #         s = Schieht(shift=shift, journal=journal, time=time, num=n)
    #         s.value = random.uniform(0, 100)
    #         s.name = gen_text()
    #         s.save()
    #
    # def fill_cinder_table(self, shift):
    #     journal = Journal.objects.get(name='Журнал экспресс анализов')
    #
    #     nums = range(2)
    #     time = parse('07.01.2017 10:00:00')
    #
    #     for n in nums:
    #         c = Cinder(shift=shift, journal=journal, time=time, col_num=n)
    #         c.shift_total = random.uniform(0, 100)
    #         c.day_total = random.uniform(0, 100)
    #         c.in_process = random.uniform(0, 100)
    #
    #         c.save()
    #
    # def fill_electrolysis_table(self, shift):
    #     journal = Journal.objects.get(name='Журнал экспресс анализов')
    #
    #     num_fields_4 = ['loads1', 'loads2', 'counter']
    #     num_fields_2 = ['bunkers_weltz', 'silos_furnace', 'bunkers_furnace']
    #     time = parse('07.01.2017 10:00:00')
    #     time1 = parse('07.01.2017 17:00:00')
    #     time2 = parse('07.01.2017 18:00:00')
    #     comment = gen_text()
    #
    #     for n in range(1, 5):
    #         e = Electrolysis(shift=shift, journal=journal, time=time, series=n)
    #         for attr in num_fields_4:
    #             setattr(e, attr, random.uniform(0, 100))
    #
    #         e.loads1 = random.randint(-1, 1)
    #         e.loads2 = random.randint(-1, 1)
    #         e.time1 = time1
    #         e.time2 = time2
    #         e.comment = comment
    #         e.save()
    #
    #     for n in range(1, 3):
    #         e = Electrolysis(shift=shift, journal=journal, time=time, series=n)
    #         for attr in num_fields_2:
    #             setattr(e, attr, random.randint(-1, 1))
    #         e.comment = comment
    #         e.save()

    # def fill_reagents_table(self, shift):
    #     journal = Journal.objects.get(name='Журнал экспресс анализов')
    #
    #     num_fields = ['shlippe', 'zn_dust', 'mg_ore', 'magnaglobe', 'fe_shave']
    #     stages = ['1st', '2st', '3st', 'cd']
    #     states = ['delivered', 'taken', 'consumption', 'issued']
    #     time = parse('07.01.2017 10:00:00')
    #     fence_state = gen_text()
    #
    #     for stg in stages:
    #         r_stg = Reagents(shift=shift, journal=journal, time=time, stage=stg)
    #         r_stg.zn_dust = random.uniform(0, 100)
    #         r_stg.state = 'none'
    #         r_stg.fence_state = fence_state
    #         r_stg.save()
    #
    #     for state in states:
    #         r = Reagents(shift=shift, journal=journal, time=time)
    #         for attr in num_fields:
    #             setattr(r, attr, random.uniform(0, 100))
    #         r.fence_state = fence_state
    #         r.state = state
    #         r.save()


    def fill_fractional_app(self, n):
        for i in range(n):
            time = timezone.now() - timedelta(hours=2 * i)
            cinder_masses = [c + random.uniform(0, 2) for c in [1, 2, 4, 7, 8, 6.5, 3, 2.5, 0.5]]
            schieht_masses = [s + random.uniform(0, 2) for s in [1, 2, 4, 7, 8, 7, 4, 3, 2, 0.5]]

            cinder_sizes = [c + random.uniform(0, 2) for c in [0.0,2.0,5.0,10.0,20.0,25.0,33.0,44.0,50.0]]
            schieht_sizes = [s + random.uniform(0, 2) for s in [0.0,2.0,5.0,10.0,20.0,25.0,33.0,44.0,50.0]]

            measurement = JournalPage.objects.create(type="measurement", date=timezone.now().today(), time = time, journal_name = "fractional_anal", plant=Plant.objects.get(name="furnace"))

            for m_value in cinder_masses:
                CellValue.objects.create(table_name="measurements", field_name='cinder_mass',
                                index=0, value=m_value, journal_page=measurement)
            for m_value in cinder_sizes:
                CellValue.objects.create(table_name="measurements", field_name='cinder_size',
                                index=0, value=m_value, journal_page=measurement)
            for m_value in schieht_masses:
                CellValue.objects.create(table_name="measurements", field_name='schieht_mass',
                                index=0, value=m_value, journal_page=measurement)
            for m_value in schieht_sizes:
                CellValue.objects.create(table_name="measurements", field_name='schieht_size',
                                index=0, value=m_value, journal_page=measurement)
           


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

    def fill_table_from_journal_page(self, journal_page, table_name, data, do_index=True):
        for field_name, values in data.items():
            if type(values) is not list:
                values = [values]

            for i, value in enumerate(values):
                index_marker_in_field_name = ""
                if type(value) is not str:
                    value = str(value)
                index = i
                CellValue(
                    journal_page=journal_page,
                    table_name=table_name,
                    field_name=field_name + index_marker_in_field_name,
                    value=value,
                    index=index
                ).save()

    def fill_upper_fields_table_jp(self, journal_page):
        table_name = "upper_fields"
        data = {
            "master": "Лупа",
            "senior_crane_operator": "Пупа",
            "storage": "12-1",
            "crane_operator": "Кто-то",
            "sling_operator": "Стив Джобс",
            "date": "10.12.12",
            "shift": "1-200-800"
        }
        self.fill_table_from_journal_page(journal_page, table_name, data)

    def fill_lower_fields_table_jp(self, journal_page):
        table_name = "lower_fields"
        data = {
            "notes": "Nice work!",
        }
        self.fill_table_from_journal_page(journal_page, table_name, data)

    def fill_big_table_jp(self, journal_page):
        table_name = "big_table"
        n = 10
        data = {
            "wagon_num": [1234] * n,
            "conc_num": ["ЗГОК"] * n,
            "supply_time": ["11:00"] * n,
            "dispatch_time": ["12:00"] * n,
            "downtime": ["12:00"] * n,
            "recieved_conc": [3] * n,
            "recieved_beds": [3] * n,
            "recieved_stops": [3] * n,
            "recieved_braces": [3] * n,
            "passed_with_shift": ["Что-нибудь"] * n
        }

        self.fill_table_from_journal_page(journal_page, table_name, data, do_index=True)

    def fill_small_table_jp(self, journal_page):
        table_name = "small_table"
        n = 10
        min, max = 10, 100
        data = {
            "storage": [1, 2],
            "containers_reciept": [randint(min, max), randint(min, max)],
            "shipped_empty_num": [randint(min, max), randint(min, max)],
            "poured_containers_num": [randint(min, max), randint(min, max)],
            "residue_empty_containers1": [randint(min, max), randint(min, max)],
            "residue_empty_containers2": [randint(min, max), randint(min, max)],
            "residue_defective_containers": [randint(min, max), randint(min, max)],
            "residue_braces": [randint(min, max), randint(min, max)],
            "residue_beds": [randint(min, max), randint(min, max)],
            "residue_stops": [randint(min, max), randint(min, max)]
        }

        self.fill_table_from_journal_page(journal_page, table_name, data)

        new_data = dict()
        for key in data.keys():
            new_data[key + "_total"] = sum(data[key])
        new_data["storage_total"] = "Итого"

        self.fill_table_from_journal_page(journal_page, table_name, new_data)



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

    def fill_journal_pages(self):
        JournalPage(
            type="shift",
            journal_name="concentrate_report_journal",
            plant=Plant.objects.get(name="furnace")).save()

    def fill_plants(self):
        Plant(name="furnace").save()
        Plant(name="electrolysis").save()
        Plant(name="leaching").save()

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

        content_type = ContentType.objects.get_for_model(CellValue)
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

    def create_settings(self):
        Setting(name="shift_count", value=2, journal="concentrate_report").save()
        Setting(name="shift_count", value=100, plant="furnace").save()

        Setting(name="background", value="Lupa", table="uchet").save()
        Setting(name="background", value="Pupa", plant="prekl").save()

        Setting(name="test", value="Aleksey", table="toble").save()


        #creating table lists for each journal
        tables_lists = { 'furnace': {'concentrate_report_journal': [],
                                   'reports_furnace_area': [],
                                   'report_income_outcome_schieht': [],
                                   'metals_compute':[] ,
                                   'technological_tasks': [],
                                   'furnace_repair': [],
                                   'furnace_changed_fraction': []},

                        'leaching': {'leaching_express_analysis': [],
                                     'leaching_repair_quipment': [],},

                        'electrolysis': {'electrolysis_repair_report_tables': [],
                                        'masters_raports': [],
                                        'electrolysis_technical_report_12_degree': [],
                                        'electrolysis_technical_report_3_degree': [],
                                        'electrolysis_technical_report_4_degree': [] } 
                                                                                        }                                                                                        
        for plant in tables_lists:
            for journal in tables_lists[plant]:
                path = f'e_logs/common/all_journals_app/templates/tables/{plant}/{journal}'
                for (dirpath, dirnames, filenames) in walk(path):
                    tables_lists[plant][journal].extend(filenames)
                    break

        for plant in tables_lists:
            for journal, tables in tables_lists[plant]:
                Setting.objects.create(name = "tables_list", value = json.dumps(tables), journal = journal)
        
        
    def clean_database(self):
        exception_models = [User, Model]
        db_models = []
        for name, obj in inspect.getmembers(famodels):
            if inspect.isclass(obj) and issubclass(obj, models.Model) and obj not in exception_models:
                db_models.append(obj)

        db_models.extend([Setting, Employee, JournalPage, CellValue, Plant, Group, Permission])

        for u in User.objects.all():  # delete user
            u.delete()

        for t in db_models:
            t.objects.all().delete()

    def create_demo_database(self, n):
        self.create_permissions_and_groups()
        self.fill_plants()
        self.fill_employees()
        self.fill_fractional_app(n)

    def recreate_database(self, *args, **kwargs):
        self.clean_database()
        self.create_demo_database()
