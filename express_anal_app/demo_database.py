import random
from itertools import product

from dateutil.parser import parse

from express_anal_app.models import *


def fill_denser_anal_table():
    shift = Shift.objects.all()[0]
    journal = Journal.objects.get(name='Журнал экспресс анализов')

    times = [parse('07.01.2017 10:00:00'), parse('07.01.2017 12:00:00'), parse('07.01.2017 18:00:00')]
    sinks = ['ls', 'hs']
    points = ['10', '11', '12']

    for t, s, p in product(times, sinks, points):
        da = DenserAnal(shift=shift, journal=journal, time=t, sink=s, point=p)
        for attr in ['ph', 'cu', 'fe', 'liq_sol']:
            setattr(da, attr, random.uniform(0, 100))
        da.save()


def fill_express_anal_table():
    shift = Shift.objects.all()[0]
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
            pe = ProductionErrors(shift=shift, journal=journal, time=t)
            for attr in ['norm', 'fact', 'error']:
                setattr(pe, attr, random.uniform(0, 100))

            pe.correction = random.choice(open('onegin.txt', encoding='utf-8').readlines())
            pe.verified = bool(random.randint(0, 1))
            pe.save()


def fill_solutions_table():
    shift = Shift.objects.all()[0]
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
        cpa.save()

        fsa = FeSolutionAnal(shift=shift, journal=journal, time=t)
        for attr in ['h2so4', 'solid', 'sb', 'cu', 'fe', 'density', 'arsenic', 'cl']:
            setattr(fsa, attr, random.uniform(0, 100))
        fsa.save()

        da = DailyAnalysis(shift=shift, journal=journal, time=t)
        for attr in ['shlippe_sb', 'activ_sas', 'circulation_denser', 'fe_hi1', 'fe_hi2']:
            setattr(da, attr, random.uniform(0, 100))
        da.save()


def fill_hydrometal1_table():
    shift = Shift.objects.all()[0]
    journal = Journal.objects.get(name='Журнал экспресс анализов')

    times = [parse('07.01.2017 10:00:00'), parse('07.01.2017 12:00:00'), parse('07.01.2017 18:00:00')]

    for t in times:
        for m in [1, 4]:
            attrs = ['ph', 'acid', 'fe2', 'fe_total'] if (m == 1) else ['ph', 'cu',  'fe2', 'sb', 'sediment']
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


def fill_agitators_table():
    shift = Shift.objects.all()[0]
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
        aa.comment = random.choice(open('onegin.txt', encoding='utf-8').readlines())
        aa.save()


def fill_neutral_table():
    shift = Shift.objects.all()[0]
    journal = Journal.objects.get(name='Журнал экспресс анализов')

    time = parse('07.01.2017 10:00:00')
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 13]

    for n in nums:
        nd = NeutralDenser(shift=shift, journal=journal, time=time, num=n)
        for attr in ['sediment', 'liq_sol1', 'liq_sol2']:
            setattr(nd, attr, random.uniform(0, 100))
        nd.save()


def fill_ready_product_table():
    shift = Shift.objects.all()[0]
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
            val = random.choice(open('onegin.txt', encoding='utf-8').readlines())
            setattr(rp, attr, val)
        rp.save()


def fill_free_tank_table():
    shift = Shift.objects.all()[0]
    journal = Journal.objects.get(name='Журнал экспресс анализов')

    nums = range(12)
    time = parse('07.01.2017 10:00:00')
    num_fields = ['prev_measure', 'cur_measure', 'deviation']
    str_fields = ['tank_name']

    for n in nums:
        ft = FreeTank(shift=shift, journal=journal, time=time, str_num=n)
        for attr in num_fields:
            setattr(ft, attr, random.uniform(0, 100))
        for attr in str_fields:
            val = open('empty-tanks.txt', encoding='utf-8').readlines()[n]
            setattr(ft, attr, val)
        ft.save()


def fill_sample2_table():
    shift = Shift.objects.all()[0]
    journal = Journal.objects.get(name='Журнал экспресс анализов')

    num_fields = ['cd', 'cu']
    times = [parse('07.01.2017 10:00:00'), parse('07.01.2017 12:00:00'),
             parse('07.01.2017 14:00:00'), parse('07.01.2017 16:00:00')]

    for t in times:
        s2 = Sample2(shift=shift, journal=journal, time=t)
        for attr in num_fields:
            setattr(s2, attr, random.uniform(0, 100))
        s2.save()


def fill_veu_table():
    shift = Shift.objects.all()[0]
    journal = Journal.objects.get(name='Журнал экспресс анализов')

    nums = range(3)
    num_fields = ['hot', 'cold']
    str_fields = ['comment']
    time = parse('07.01.2017 10:00:00')

    for n in nums:
        veu = VEU(shift=shift, journal=journal, time=time)
        for attr in num_fields:
            setattr(veu, attr, random.uniform(0, 100))
        for attr in str_fields:
            val = random.choice(open('onegin.txt', encoding='utf-8').readlines())
            setattr(veu, attr, val)
        veu.save()


def fill_neutral_solution_table():
    shift = Shift.objects.all()[0]
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
            val = random.choice(open('onegin.txt', encoding='utf-8').readlines())
            setattr(ns, attr, val)
        ns.save()


def fill_shift_info_table():
    shift = Shift.objects.all()[0]
    journal = Journal.objects.get(name='Журнал экспресс анализов')

    time = parse('07.01.2017 10:00:00')
    num_fields = ['out_sol_t', 'out_sol_c', 'out_pulp_cvck', 'out_cu_kek', 'out_cd_sponge',
                  'out_electr', 'out_ruch_cd', 'out_neutr', 'out_cu_pulp', 'in_filtrate_ls', 'in_filtrate_dens',
                  'in_fe', 'in_fe_hi', 'in_poor_cd']

    si = ShiftInfo(shift=shift, journal=journal, time=time)
    for attr in num_fields:
        setattr(si, attr, random.uniform(0, 100))
    si.save()


def fill_self_sequrity_table():
    shift = Shift.objects.all()[0]
    journal = Journal.objects.get(name='Журнал экспресс анализов')

    times = [parse('07.01.2017 10:00:00'), parse('07.01.2017 12:00:00'), parse('07.01.2017 14:00:00')]
    onegin = open('onegin.txt', encoding='utf-8').readlines(); rr = random.randint(0, len(onegin)-1)
    bignote = ''.join(onegin[rr:rr+4])

    for t in times:
        ss = SelfSecurity(shift=shift, journal=journal, time=t)
        ss.note = random.choice(open('onegin.txt', encoding='utf-8').readlines())
        ss.bignote = bignote
        ss.save()


def fill_scheiht_table():
    shift = Shift.objects.all()[0]
    journal = Journal.objects.get(name='Журнал экспресс анализов')

    nums = range(3)
    time = parse('07.01.2017 10:00:00')

    for n in nums:
        s = Schieht(shift=shift, journal=journal, time=time, num=n)
        s.value = random.uniform(0, 100)
        s.name = random.choice(open('onegin.txt', encoding='utf-8').readlines())
        s.save()


def clean_database():
    model_tables = [
        DenserAnal,  # densers table
        ProductionErrors, LeachingExpressAnal,  # express anal table
        ZnPulpAnal, CuPulpAnal, FeSolutionAnal, DailyAnalysis,  # solutions table
        HydroMetal, CinderDensity,  # for hydrometal
        Agitators,
        NeutralDenser,
        ReadyProduct,
        FreeTank,
        VEU,
        Sample2,
        NeutralSolution,
        ShiftInfo,
        Schieht,
        SelfSecurity,
    ]

    for t in model_tables:
        t.objects.all().delete()


def fill_database():
    fill_express_anal_table()
    fill_denser_anal_table()
    fill_solutions_table()
    fill_hydrometal1_table()
    fill_agitators_table()
    fill_neutral_table()
    fill_ready_product_table()
    fill_free_tank_table()
    fill_veu_table()
    fill_sample2_table()
    fill_neutral_solution_table()
    fill_shift_info_table()
    fill_self_sequrity_table()
    fill_scheiht_table()
