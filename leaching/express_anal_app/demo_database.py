import inspect
import random
from datetime import timedelta
from inspect import ismethod
from itertools import product

from django.db.models import Model
from django.utils import timezone

from furnace.fractional_app.models import *
from furnace.fractional_app import models as famodels
from leaching.express_anal_app import models as eamodels
from leaching.repair_app import models as remodels
from leaching.express_anal_app.models import *
from common.all_journals_app import models as comodels
from common.all_journals_app.models import *
from leaching.repair_app.models import *
from utils.webutils import parse, translate
from django.utils.translation import gettext as _

onegin = None


def gen_text(lines=1, max_words=10):
    global onegin
    if onegin is None:
        onegin = open('onegin.txt', encoding='utf-8').readlines()
        onegin = filter(lambda x: 50 > len(x.strip()) > 10, onegin)
        onegin = [s.strip() for s in onegin]

    num = random.randint(0, len(onegin) - lines)
    lines = onegin[num:num + lines]
    lines = [' '.join(l.split()[:max_words]) for l in lines]
    return '\n'.join(lines)


class DatabaseFiller:
    """
    All fill methods names and only they should be like 'fill_*_table'.
    Filling methods will be called in a random order
    """

    def fill_denser_anal_table(self, shift):
        journal = Journal.objects.get(name='Журнал экспресс анализов')

        times = [parse('07.01.2017 10:00:00'), parse('07.01.2017 12:00:00'), parse('07.01.2017 18:00:00')]
        sinks = ['ls', 'hs']
        points = ['10', '11', '12']

        for t, s, p in product(times, sinks, points):
            da = DenserAnal(shift=shift, journal=journal, time=t, sink=s, point=p)
            for attr in ['ph', 'cu', 'fe', 'liq_sol']:
                setattr(da, attr, random.uniform(0, 100))
            da.save()

    def fill_express_anal_table(self, shift):
        journal = Journal.objects.get(name='Журнал экспресс анализов')

        times = [parse('07.01.2017 10:00:00'), parse('07.01.2017 12:00:00'), parse('07.01.2017 18:00:00')]
        points = ['lshs', 'larox', 'purified', 'prod_correction']

        for t, p in product(times, points):
            lea = LeachingExpressAnal(shift=shift, journal=journal, time=t, point=p)
            if p == 'lshs':
                for attr in ['co', 'sb', 'cu', 'cu_st1', 'cd', 'solid_st1', 'ph', 'fe', 'arsenic', 'solid', 'density']:
                    setattr(lea, attr, random.uniform(0, 100))
            elif p == 'larox':
                for attr in ['co', 'sb', 'cd', 'solid', 'ph']:
                    setattr(lea, attr, random.uniform(0, 100))
            elif p == 'purified':
                for attr in ['cd', 'co', 'sb', 'cu', 'fe', 'current', 'density', '']:
                    setattr(lea, attr, random.uniform(0, 100))
            lea.save()

            if p == 'prod_correction':
                pe = ProductionError(shift=shift, journal=journal, time=t)
                for attr in ['norm', 'fact', 'error']:
                    setattr(pe, attr, random.uniform(0, 100))

                pe.correction = gen_text()
                pe.verified = bool(random.randint(0, 1))
                pe.save()

    def fill_solutions_table(self, shift):
        journal = Journal.objects.get(name='Журнал экспресс анализов')

        times = [parse('07.01.2017 10:00:00'), parse('07.01.2017 12:00:00'), parse('07.01.2017 18:00:00')]

        for t in times:
            zpa = ZnPulpAnal(shift=shift, journal=journal, time=t)
            for attr in ['liq_sol', 'ph', 't0']:
                setattr(zpa, attr, random.uniform(0, 100))
            zpa.save()

            cpa = CuPulpAnal(shift=shift, journal=journal, time=t)
            for attr in ['liq_sol', 'before', 'after', 'solid']:
                setattr(cpa, attr, random.uniform(0, 100))
            cpa.zn_pulp_anal = zpa
            cpa.save()

            fsa = FeSolutionAnal(shift=shift, journal=journal, time=t)
            for attr in ['h2so4', 'solid', 'sb', 'cu', 'fe', 'density', 'arsenic', 'cl']:
                setattr(fsa, attr, random.uniform(0, 100))
            fsa.zn_pulp_anal = zpa
            fsa.cu_pulp_anal = cpa
            fsa.save()

            da = DailyAnalysis(shift=shift, journal=journal, time=t)
            for attr in ['shlippe_sb', 'activ_sas', 'circulation_denser', 'fe_hi1', 'fe_hi2']:
                setattr(da, attr, random.uniform(0, 100))
            da.save()

    def fill_hydrometal1_table(self, shift):
        journal = Journal.objects.get(name='Журнал экспресс анализов')

        times = [parse('07.01.2017 10:00:00'), parse('07.01.2017 12:00:00'), parse('07.01.2017 18:00:00')]

        for t in times:
            for m in [1, 4]:
                attrs = ['ph', 'acid', 'fe2', 'fe_total'] if (m == 1) else ['ph', 'cu', 'fe2', 'sb', 'sediment']
                hm = HydroMetal(shift=shift, journal=journal, time=t, mann_num=m)
                for attr in attrs:
                    setattr(hm, attr, random.uniform(0, 100))
                hm.employee = shift.laborant
                hm.save()

            attrs = ['gran', 'gran_avg', 'fe_avg', 'fe_shave']
            cd = CinderDensity(shift=shift, journal=journal, time=t)
            for attr in attrs:
                setattr(cd, attr, random.uniform(0, 100))
            cd.employee = shift.laborant
            cd.save()

    def fill_agitators_table(self, shift):
        journal = Journal.objects.get(name='Журнал экспресс анализов')

        times = [parse('07.01.2017 10:00:00'), parse('07.01.2017 12:00:00'), parse('07.01.2017 18:00:00')]
        nums = [13, 15, 17, 19]

        for t, n, b in product(times, nums, (True, False)):
            if n == 13:
                attrs = ['cd', 'cu', 'co']
            elif n == 15:
                attrs = ['ph', 'cu']
            elif n == 17:
                attrs = ['ph', 'cu']
            else:
                attrs = ['h2so4', 'cu']

            aa = Agitators(shift=shift, journal=journal, time=t, num=n, before=b)
            for attr in attrs:
                setattr(aa, attr, random.uniform(0, 100))

            aa.employee = shift.laborant
            aa.comment = gen_text()
            aa.save()

    def fill_neutral_table(self, shift):
        journal = Journal.objects.get(name='Журнал экспресс анализов')

        time = parse('07.01.2017 10:00:00')
        nums = [1, 2, 3, 4, 5, 6, 7, 8, 13]

        for n in nums:
            nd = NeutralDenser(shift=shift, journal=journal, time=time, num=n)
            for attr in ['sediment', 'liq_sol1', 'liq_sol2']:
                setattr(nd, attr, random.uniform(0, 100))
            nd.save()

    def fill_ready_product_table(self, shift):
        journal = Journal.objects.get(name='Журнал экспресс анализов')

        time = parse('07.01.2017 10:00:00')
        num_fields = ['cd', 'cu', 'co', 'sb', 'fe', 'vt', 'density', 'norm', 'fact']
        str_fields = ['correction']
        nums = [3, 4, 5]

        for n in nums:
            rp = ReadyProduct(shift=shift, journal=journal, time=time, num=n)
            for attr in num_fields:
                setattr(rp, attr, random.uniform(0, 100))
            for attr in str_fields:
                val = gen_text()
                setattr(rp, attr, val)
            rp.save()

    def fill_free_tank_table(self, shift):
        journal = Journal.objects.get(name='Журнал экспресс анализов')

        nums = range(12)
        time = parse('07.01.2017 10:00:00')
        num_fields = ['prev_measure', 'cur_measure', 'deviation']
        str_fields = ['tank_name']

        names = [_('Бак отработ. 1-2 серий'), _('Манны №1-9'), _('Манны ВТВ №10-12'),
                 _('Обор-й сгуститель №9'), _('Агитатор 22'), _('Бак нейтр. р-ра, 1-й цех'),
                 _('Ман отраб. № 2, 1-й цех'), _('Ман отраб. № 3, 1-й цех'), _('Ман отраб. № 9, 1-й цех'),
                 _('-'), _('СМЕННЫЙ БАЛАНС'), _('СУТОЧНЫЙ БАЛАНС')]

        for n in nums:
            ft = FreeTank(shift=shift, journal=journal, time=time, str_num=n)
            for attr in num_fields:
                setattr(ft, attr, random.uniform(0, 100))
            for attr in str_fields:
                val = names[n]
                setattr(ft, attr, val)
            ft.save()

    def fill_sample2_table(self, shift):
        journal = Journal.objects.get(name='Журнал экспресс анализов')

        num_fields = ['cd', 'cu']
        times = [parse('07.01.2017 10:00:00'), parse('07.01.2017 12:00:00'),
                 parse('07.01.2017 14:00:00'), parse('07.01.2017 16:00:00')]

        for t in times:
            s2 = Sample2(shift=shift, journal=journal, time=t)
            for attr in num_fields:
                setattr(s2, attr, random.uniform(0, 100))
            s2.save()

    def fill_veu_table(self, shift):
        journal = Journal.objects.get(name='Журнал экспресс анализов')

        nums = range(3)
        num_fields = ['hot', 'cold']
        str_fields = ['comment']
        time = parse('07.01.2017 10:00:00')

        for n in nums:
            veu = VEU(shift=shift, journal=journal, time=time, num=n)
            for attr in num_fields:
                setattr(veu, attr, random.uniform(0, 100))
            for attr in str_fields:
                val = gen_text()
                setattr(veu, attr, val)
            veu.save()

    def fill_neutral_solution_table(self, shift):
        journal = Journal.objects.get(name='Журнал экспресс анализов')

        nums = range(9)
        num_fields = ['value']
        str_fields = ['tank_name']
        time = parse('07.01.2017 10:00:00')

        for n in nums:
            ns = NeutralSolution(shift=shift, journal=journal, time=time, str_num=n)
            for attr in num_fields:
                setattr(ns, attr, random.uniform(0, 100))
            for attr in str_fields:
                val = gen_text()
                setattr(ns, attr, val)
            ns.save()

    def fill_shift_info_table(self, shift):
        journal = Journal.objects.get(name='Журнал экспресс анализов')

        time = parse('07.01.2017 10:00:00')
        num_fields = ['out_sol_t', 'out_sol_c', 'out_pulp_cvck', 'out_cu_kek', 'out_cd_sponge',
                      'out_electr', 'out_ruch_cd', 'out_neutr', 'out_cu_pulp', 'in_filtrate_ls', 'in_filtrate_dens',
                      'in_fe', 'in_fe_hi', 'in_poor_cd', 'free_13', 'free_14']

        si = ShiftInfo(shift=shift, journal=journal, time=time)
        for attr in num_fields:
            setattr(si, attr, random.uniform(0, 100))

        si.this_master = Employee.objects.all()[0]
        si.next_master = Employee.objects.all()[1]
        si.furnaces = '45'
        si.free_13_t = '3'
        si.free_14_t = '0ч'

        si.save()

    def fill_self_sequrity_table(self, shift):
        journal = Journal.objects.get(name='Журнал экспресс анализов')

        times = [parse('07.01.2017 12:00:00'), parse('07.01.2017 14:00:00'), parse('07.01.2017 16:00:00')]
        bignote = gen_text(lines=4)

        for t in times:
            ss = SelfSecurity(shift=shift, journal=journal, time=t)
            ss.note = gen_text()
            ss.bignote = bignote
            ss.save()

    def fill_scheiht_table(self, shift):
        journal = Journal.objects.get(name='Журнал экспресс анализов')

        nums = range(3)
        time = parse('07.01.2017 10:00:00')

        for n in nums:
            s = Schieht(shift=shift, journal=journal, time=time, num=n)
            s.value = random.uniform(0, 100)
            s.name = gen_text()
            s.save()

    def fill_cinder_table(self, shift):
        journal = Journal.objects.get(name='Журнал экспресс анализов')

        nums = range(2)
        time = parse('07.01.2017 10:00:00')

        for n in nums:
            c = Cinder(shift=shift, journal=journal, time=time, col_num=n)
            c.shift_total = random.uniform(0, 100)
            c.day_total = random.uniform(0, 100)
            c.in_process = random.uniform(0, 100)

            c.save()

    def fill_electrolysis_table(self, shift):
        journal = Journal.objects.get(name='Журнал экспресс анализов')

        num_fields_4 = ['loads1', 'loads2', 'counter']
        num_fields_2 = ['bunkers_weltz', 'silos_furnace', 'bunkers_furnace']
        time = parse('07.01.2017 10:00:00')
        time1 = parse('07.01.2017 17:00:00')
        time2 = parse('07.01.2017 18:00:00')
        comment = gen_text()

        for n in range(1, 5):
            e = Electrolysis(shift=shift, journal=journal, time=time, series=n)
            for attr in num_fields_4:
                setattr(e, attr, random.uniform(0, 100))

            e.loads1 = random.randint(-1, 1)
            e.loads2 = random.randint(-1, 1)
            e.time1 = time1
            e.time2 = time2
            e.comment = comment
            e.save()

        for n in range(1, 3):
            e = Electrolysis(shift=shift, journal=journal, time=time, series=n)
            for attr in num_fields_2:
                setattr(e, attr, random.randint(-1, 1))
            e.comment = comment
            e.save()

    def fill_reagents_table(self, shift):
        journal = Journal.objects.get(name='Журнал экспресс анализов')

        num_fields = ['shlippe', 'zn_dust', 'mg_ore', 'magnaglobe', 'fe_shave']
        stages = ['1st', '2st', '3st', 'cd']
        states = ['delivered', 'taken', 'consumption', 'issued']
        time = parse('07.01.2017 10:00:00')
        fence_state = gen_text()

        for stg in stages:
            r_stg = Reagents(shift=shift, journal=journal, time=time, stage=stg)
            r_stg.zn_dust = random.uniform(0, 100)
            r_stg.state = 'none'
            r_stg.fence_state = fence_state
            r_stg.save()

        for state in states:
            r = Reagents(shift=shift, journal=journal, time=time)
            for attr in num_fields:
                setattr(r, attr, random.uniform(0, 100))
            r.fence_state = fence_state
            r.state = state
            r.save()


    def fill_fractional_app(self):
        cinder_base = [1, 2, 4, 7, 8, 6.5, 3, 2.5, 0.5]
        schieht_base = [1, 2, 4, 7, 8, 7, 4, 3, 2, 0.5]
        for i in range(100):
            time = timezone.now() - datetime.timedelta(hours=2 * i)
            cinder = [c + random.uniform(0, 2) for c in cinder_base]
            schieht = [s + random.uniform(0, 2) for s in schieht_base]

            mp = MeasurementPair().add_weights(cinder, schieht, time, time - datetime.timedelta(minutes=30))
            mp.save()


    def fill_equipement(self):
        eq_list = [
            'Агитатор «Манн» №1',
            'Агитатор «Манн» №2',
            'Агитатор «Манн» №3',
            'Сгуститель №1',
            'Сгуститель №2',
            'Сгуститель №3',
            'Питатель ленточный В – 500 мм',
            'Элеватор ЦГ-400 №1',
            'Элеватор ЦГ-400 №2',
            'Транспортер ленточный В – 650 мм',
        ]

        for e in eq_list:
            Equipment(name=e).save()

    def fill_leaching_repairs(self):
        equipments = list(Equipment.objects.all())
        for i in range(100):
            r = Repairs()
            r.equipment = random.choice(equipments)
            date = timezone.now() - timedelta(days=random.randint(0, 400))
            r.date = date
            r.date_performed = date
            r.name = gen_text(max_words=7)
            r.comment = gen_text(max_words=15)
            r.save()

    def fill_big_table_jp(self, journal_page):
        table_name = "big table"
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

        for field_name, values in data.items():
            for value in values:
                if type(value) is not str:
                    value = str(value)
                v = CellValue(
                    journal_page=journal_page,
                    table_name=table_name,
                    field_name=field_name,
                    value=value).save()


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
            e.plant = 'leaching'
            lname = translate(e.name).replace(' ', '_')
            e.user = User.objects.create_user(lname, lname + '@kazzink.kz', lname)
            e.save()

        for f, l in product(ru_names, ru_l_names):
            e = Employee()
            e.name = f + ' ' + l
            e.position = 'master'
            e.plant = 'leaching'
            lname = translate(e.name).replace(' ', '_')
            e.user = User.objects.create_user(lname, lname + '@kazzink.kz', lname)
            e.save()

        for f, l in product(kz_names, ru_l_names):
            e = Employee()
            e.name = f + ' ' + l
            e.position = 'hydro'
            e.plant = 'leaching'
            lname = translate(e.name).replace(' ', '_')
            e.user = User.objects.create_user(lname, lname + '@kazzink.kz', lname)
            e.save()

    def fill_journals(self):
        Journal(name='Журнал экспресс анализов',
                description='Журнал экспресс анализов в цехе выщелачивания', plant='leaching').save()
        Journal(name='Журнал планового ремонта',
                description='Журнал планового ремонта в цехе выщелачивания', plant='leaching').save()
        Journal(name='Журнал капитального ремонта',
                description='Журнал капитального в цехе выщелачивания', plant='leaching').save()
        Journal(name='Журнал обжига',
                description='Журнал обжига в цехе обжига', plant='furnace').save()

    def fill_journal_pages(self):
        JournalPage(type="shift", journal_name="Журнал рапортов").save()

    def fill_shifts(self):
        dates = [parse('10-10-2015'), parse('12-10-2015')]

        for i in range(4):
            sh = Shift()
            sh.date = dates[i % 2]
            sh.plant = 'leaching'
            sh.order = random.randint(1, 2)
            sh.master = random.choice(Employee.objects.filter(position='master'))
            sh.laborant = random.choice(Employee.objects.filter(position='laborant'))
            sh.hydro = random.choice(Employee.objects.filter(position='hydro'))
            sh.save()

    def fill_shift_data(self, shift):
        for name in dir(self):
            attribute = getattr(self, name)
            if ismethod(attribute) and name.startswith('fill_') and name.endswith('_table'):
                attribute(shift=shift)

    def fill_journalpages_data(self, journal_page):
        for name in dir(self):
            attribute = getattr(self, name)
            if ismethod(attribute) and name.startswith('fill_') and name.endswith('_table_jp'):
                attribute(journal_page=journal_page)


    def clean_database(self):
        exception_models = [User, Employee, Shift, Journal, JournalTable, Model]

        db_models = []
        for name, obj in inspect.getmembers(eamodels):
            if inspect.isclass(obj) and issubclass(obj, models.Model) and obj not in exception_models:
                db_models.append(obj)

        for name, obj in inspect.getmembers(famodels):
            if inspect.isclass(obj) and issubclass(obj, models.Model) and obj not in exception_models:
                db_models.append(obj)

        for name, obj in inspect.getmembers(remodels):
            if inspect.isclass(obj) and issubclass(obj, models.Model) and obj not in exception_models:
                db_models.append(obj)

        db_models.extend([Journal, Shift, Employee])
        db_models.extend([JournalPage, CellValue])

        for u in User.objects.all():  # delete user
            if not u.is_superuser:
                u.delete()

        for t in db_models:
            t.objects.all().delete()

    def create_demo_database(self):
        # create journal and shift
        self.fill_employees()
        self.fill_journals()
        self.fill_journal_pages()
        self.fill_shifts()

        self.fill_fractional_app()
        self.fill_equipement()
        self.fill_leaching_repairs()

        for sh in Shift.objects.all():
            self.fill_shift_data(shift=sh)

        for jp in JournalPage.objects.all():
            self.fill_journalpages_data(journal_page=jp)


    def recreate_database(self, *args, **kwargs):
        self.clean_database()
        self.create_demo_database()
