import time
from django.contrib.auth.models import User
from django.db import models


# TODO: Do we set null=TRUE?
from login_app.models import Employee


class Journal(models.Model):
    name = models.CharField(max_length=1000, blank=False, null=False)
    description = models.TextField()


class Shift(models.Model):
    order = models.DecimalField(max_digits=1, decimal_places=0)
    master = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='leaching_shift_masters')
    laborant = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='leaching_shift_labornats')
    plant = models.CharField(max_length=1, choices=(('0', 'furnace'),
                                                    ('1', 'leaching'),
                                                    ('2', 'electrolysis'),))


class JournalTable(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True)
    time = models.DateTimeField()
    journal = models.ForeignKey(Journal, on_delete=models.SET_NULL, null=True)


# Low Sink High Sink
class LeachingExpressAnal(JournalTable):  # The name is shit!
    point = models.CharField(max_length=1, choices=(('0', 'lshs'),
                                                    ('1', 'larox'),
                                                    ('2', 'purified'),
                                                    ('3', 'errors'),))

    co = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    sb = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    cu = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    cu_st1 = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    cd = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    solid_st1 = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    ph = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    fe = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    arsenic = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    solid = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    density = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    current = models.DecimalField(max_digits=10, decimal_places=5, blank=True)


class ProductionErrors(JournalTable):
    norm = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    fact = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    error = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    correction = models.CharField(max_length=512)
    verified = models.BooleanField(default=False)


class DenserAnal(JournalTable):
    point = models.CharField(max_length=1, choices=(('0', '10'),
                                                    ('1', '11'),
                                                    ('2', '12'),))

    sink = models.CharField(max_length=1, choices=(('0', 'upper'),
                                                    ('1', 'lower')))
    ph = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    cu = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    fe = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    liq_sol = models.DecimalField(max_digits=10, decimal_places=5, blank=True)


class ZnPulpAnal(JournalTable):
    liq_sol = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    ph = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    t0 = models.DecimalField(max_digits=10, decimal_places=5, blank=True)


class CuPulpAnal(JournalTable):  # TODO: comment?? shitti values
    liq_sol = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    before = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    after = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    solid = models.DecimalField(max_digits=10, decimal_places=5, blank=True)


class FeSolutionAnal(JournalTable):
    h2so4 = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    solid = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    sb = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    cu = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    fe = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    density = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    As = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    Cl = models.DecimalField(max_digits=10, decimal_places=5, blank=True)


class DailyAnalysis(JournalTable):  # shit next to Fe
    shlippe_sb = models.CharField(max_length=64, blank=True)
    activ_sas = models.CharField(max_length=64, blank=True)  # SAS is how american shitheads call ПАВ
    circulation_denser = models.CharField(max_length=64, blank=True)
    fe_hi1 = models.CharField(max_length=64, blank=True)
    fe_hi2 = models.CharField(max_length=64, blank=True)


class HydroMetal(JournalTable):
    ph = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    acid = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    fe2 = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    fe_total = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    cu = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    sb = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    sediment = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    mann_num = models.DecimalField(max_digits=10, decimal_places=5, blank=True)

    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)


class CinderDensity(JournalTable):
    gran = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    gran_avg = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    fe_avg = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    fe_shave = models.DecimalField(max_digits=10, decimal_places=5, blank=True)

    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)


class Agitators(JournalTable):
    before = models.BooleanField()
    ph = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    cu = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    co = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    cd = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    h2so4 = models.DecimalField(max_digits=10, decimal_places=5, blank=True)  # here they write % symbol
    comment = models.DecimalField(max_digits=10, decimal_places=5, blank=True)

    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)  # maybe this should be in shift info


class NeutralDenser(JournalTable):
    num = models.DateTimeField()
    sediment = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    liq_sol1 = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    liq_sol2 = models.DecimalField(max_digits=10, decimal_places=5, blank=True)


class ReadyProduct(JournalTable):
    num = models.DecimalField(max_digits=1, decimal_places=0, blank=True)
    cd = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    cu = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    co = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    sb = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    fe = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    vt = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    density = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    norm = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    fact = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    correction = models.CharField(max_length=128, blank=True)
    verified = models.DecimalField(max_digits=10, decimal_places=5, blank=True)


class Reagents(JournalTable):  # TODO: Надо осмыслить эту их писанину
    shlippe = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    zn = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    mg = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    magnaglobe = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    fe_shave = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    fence_state = models.CharField(max_length=255, blank=True)

    delivered = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    accepted = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    consumption = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    taken_away = models.DecimalField(max_digits=10, decimal_places=5, blank=True)

    stage = models.CharField(max_length=1, choices=(('0', '1'),
                                                    ('1', '2'),
                                                    ('2', '3'),
                                                    ('3', 'cd'),
                                                    ('4', 'empty'),))


class VEU(JournalTable):
    hot = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    cold = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    comment = models.CharField(max_length=128, blank=True)


class Sample2(JournalTable):
    cd = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    cu = models.DecimalField(max_digits=10, decimal_places=5, blank=True)


class FreeTank(JournalTable):
    tank_name = models.CharField(max_length=128, blank=True)
    prev_measure = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    deviation = models.DecimalField(max_digits=10, decimal_places=5, blank=True)


class SelfSecurity(JournalTable):
    note = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    bignote = models.DecimalField(max_digits=10, decimal_places=5, blank=True)


class Electrolysis(JournalTable):
    series = models.DateTimeField()
    loads1 = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    loads2 = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    counter = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    bunkers_weltz = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    silos_furnace = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    bunkers_furnace = models.DecimalField(max_digits=10, decimal_places=5, blank=True)


class ShiftInfo(JournalTable):
    out_sol_t = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    out_sol_c = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    out_pulp_cvck = models.DecimalField(max_digits=10, decimal_places=5, blank=True)  # TODO: fuck!
    out_cu_kek = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    out_cd_sponge = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    out_electr = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    out_ruch_cd = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    out_neutr = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    out_cu_pulp = models.DecimalField(max_digits=10, decimal_places=5, blank=True)

    in_filtrate_ls = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    in_filtrate_dens = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    in_fe = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    in_fe_hi = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    in_poor_cd = models.DecimalField(max_digits=10, decimal_places=5, blank=True)


class Schieht(JournalTable):
    num = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    name = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=5, blank=True)


class NeutralSolution(JournalTable):  # should it be text
    tank_name = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=5, blank=True)

