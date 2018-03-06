import random
from itertools import product

from dateutil.parser import parse

from express_anal_app.models import DenserAnal, Shift, Journal, LeachingExpressAnal, ProductionErrors, ZnPulpAnal, \
    CuPulpAnal, FeSolutionAnal, DailyAnalysis


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

            pe.correction = random.choice(open('manage.py').readlines())
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


def clean_database():
    model_tables = [
        DenserAnal,  # densers table
        ProductionErrors, LeachingExpressAnal,  # express anal table
        ZnPulpAnal, CuPulpAnal, FeSolutionAnal, DailyAnalysis  # solutions table
    ]

    for t in model_tables:
        t.objects.all().delete()


def fill_database():
    fill_express_anal_table()
    fill_denser_anal_table()
    fill_solutions_table()
