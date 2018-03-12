import time

from decimal import Decimal
from django.contrib.auth.models import User
from django.db import models

# TODO: Do we set null=TRUE?
from login_app.models import Employee


class Journal(models.Model):
    name = models.CharField(max_length=1000, blank=False, null=False, verbose_name='Название журнала')
    description = models.TextField(verbose_name='Описание таблицы')

    def __str__(self):
        return self.name


class Shift(models.Model):
    date = models.DateField(verbose_name='Дата начала смены')
    order = models.DecimalField(max_digits=1, decimal_places=0, verbose_name='Номер смены (1, 2)')
    master = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True,
                               related_name='leaching_shift_masters', verbose_name='Мастер смены')
    laborant = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True,
                                 related_name='leaching_shift_labornats', verbose_name='Лаборант')
    plant = models.CharField(max_length=10, verbose_name='Цех', choices=(('furnace', 'обжиг'),
                                                                         ('leaching', 'выщелачивание'),
                                                                         ('electrolysis', 'электролиз'),))

    def __str__(self):
        return f'<{self.date}> {self.order} смена, {self.get_plant_display()}'


class JournalTable(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, verbose_name='Смена')
    time = models.DateTimeField('Время анализа/создания записи')
    journal = models.ForeignKey(Journal, on_delete=models.SET_NULL, null=True, verbose_name='Журнал')

    def __str__(self):
        return f'{self.journal}, запись {self.time}'


# Low Sink High Sink
class LeachingExpressAnal(JournalTable):  # The name is shit!
    point = models.CharField(max_length=20, verbose_name='Место измерения', choices=(('0', 'lshs'),
                                                                                     ('larox', 'Ларокс'),
                                                                                     ('purified', 'Очищенный раствор'),
                                                                                     ('prod_correction',
                                                                                      'Упр. Несоответствия продукции'),))

    co = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='Co')
    sb = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='Sb')
    cu = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='Cu')
    cu_st1 = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='Cu ст.1')
    cd = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='Cd')
    solid_st1 = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='Cd')
    ph = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='pH')
    fe = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='Fe')
    arsenic = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='As')
    solid = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='Твердое г\л')
    current = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='Выход по току')
    density = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='Уд. вес')


class ProductionErrors(JournalTable):
    norm = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='Норма')
    fact = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='Факт')
    error = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='Несоответствие')
    correction = models.CharField(max_length=512, verbose_name='Коррекция')
    verified = models.BooleanField(default=False, verbose_name='Проверено')


class DenserAnal(JournalTable):
    point = models.CharField(max_length=20, verbose_name='Сгуститель №', choices=(('10', 'Сгуститель №10'),
                                                                                  ('11', 'Сгуститель №11'),
                                                                                  ('12', 'Сгуститель №12'),))

    sink = models.CharField(max_length=5, verbose_name='Слив', choices=(('ls', 'НС'),
                                                                        ('hs', 'ВС')))
    ph = models.DecimalField(max_digits=10, verbose_name='pH', decimal_places=5, blank=True, null=True)
    cu = models.DecimalField(max_digits=10, verbose_name='Cu', decimal_places=5, blank=True, null=True)
    fe = models.DecimalField(max_digits=10, verbose_name='Fe', decimal_places=5, blank=True, null=True)
    liq_sol = models.DecimalField(max_digits=10, verbose_name='Ж:Т', decimal_places=5, blank=True, null=True)


class ZnPulpAnal(JournalTable):
    liq_sol = models.DecimalField(max_digits=10, decimal_places=5, blank=True, verbose_name='Ж:Т')
    ph = models.DecimalField(max_digits=10, decimal_places=5, blank=True, verbose_name='pH')
    t0 = models.DecimalField(max_digits=10, decimal_places=5, blank=True, verbose_name='t0')


class CuPulpAnal(JournalTable):  # TODO: comment?? shitti values
    liq_sol = models.DecimalField(max_digits=10, decimal_places=5, blank=True, verbose_name='Ж:Т')
    before = models.DecimalField(max_digits=10, decimal_places=5, blank=True, verbose_name='До')
    after = models.DecimalField(max_digits=10, decimal_places=5, blank=True, verbose_name='После')
    solid = models.DecimalField(max_digits=10, decimal_places=5, blank=True, verbose_name='ТВ')


class FeSolutionAnal(JournalTable):
    h2so4 = models.DecimalField(max_digits=10, decimal_places=5, blank=True, verbose_name='H2SO4')
    solid = models.DecimalField(max_digits=10, decimal_places=5, blank=True, verbose_name='ТВ')
    sb = models.DecimalField(max_digits=10, decimal_places=5, blank=True, verbose_name='Sb')
    cu = models.DecimalField(max_digits=10, decimal_places=5, blank=True, verbose_name='Cu')
    fe = models.DecimalField(max_digits=10, decimal_places=5, blank=True, verbose_name='Fe')
    density = models.DecimalField(max_digits=10, decimal_places=5, blank=True, verbose_name='Уд. вес')
    arsenic = models.DecimalField(max_digits=10, decimal_places=5, blank=True, verbose_name='As')
    cl = models.DecimalField(max_digits=10, decimal_places=5, blank=True, verbose_name='Cl')


class DailyAnalysis(JournalTable):  # shit next to Fe
    shlippe_sb = models.CharField(max_length=64, blank=True, verbose_name='Концентрация Sb в р-ре соли Шлиппе')
    activ_sas = models.CharField(max_length=64, blank=True, verbose_name='Активность ПАВ')
    circulation_denser = models.CharField(max_length=64, blank=True, verbose_name='Анализы оборот. сгуст.')
    fe_hi1 = models.CharField(max_length=64, blank=True, verbose_name='Высоко Fe р-р')
    fe_hi2 = models.CharField(max_length=64, blank=True, verbose_name='Высоко Fe р-р 2')


class HydroMetal(JournalTable):
    ph = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='pH')
    acid = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='Кисл-ть')
    fe2 = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='Fe двухвал')
    fe_total = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='Fe общее')
    cu = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='Медь')
    sb = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='Сурьма')
    sediment = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='Отстой')
    mann_num = models.DecimalField(max_digits=1, decimal_places=0, blank=True,
                                   null=True, verbose_name='Манн №', choices=((1, '1 Манн'), (4, '4 Манн')))

    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL,
                                 null=True, verbose_name='Аппаратчик-гидрометаллург')


class CinderDensity(JournalTable):
    gran = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='Ситовой огарка')
    gran_avg = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True,
                                   verbose_name='Ситовой огарка средний')
    fe_avg = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True,
                                 verbose_name='Общее Fe среднее')
    fe_shave = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='Fe Стружка Fe')

    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL,
                                 null=True, verbose_name='Аппаратчик-гидрометаллург')


class Agitators(JournalTable):
    num = models.CharField(max_length=20, blank=False, null=True, verbose_name='Агитатор', choices=(('13', '13, 14'),
                                                                                                    ('15', '15'),
                                                                                                    ('17', '17'),
                                                                                                    ('19', '19'),))
    before = models.BooleanField(verbose_name='До')
    ph = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='pH')
    cu = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='Cu')
    co = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='Co')
    cd = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='Cd')
    h2so4 = models.DecimalField(max_digits=10, decimal_places=5,
                                blank=True, null=True, verbose_name='H2SO4')  # here they write % symbol
    comment = models.CharField(max_length=128, blank=True, verbose_name='Комментарий')

    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL,  # мб их в shift_info
                                 null=True, verbose_name='Аппаратчик-гидрометаллург')


class NeutralDenser(JournalTable):
    num = models.DecimalField(max_digits=2, decimal_places=0)
    sediment = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    liq_sol1 = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    liq_sol2 = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)


class ReadyProduct(JournalTable):
    num = models.DecimalField(max_digits=1, decimal_places=0, blank=True, null=True)
    cd = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    cu = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    co = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    sb = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    fe = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    vt = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    density = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    norm = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    fact = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    correction = models.CharField(max_length=128, blank=True, null=True)
    verified = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)


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

    stage = models.CharField(max_length=20, choices=(('1', '1ст'),
                                                     ('2', '2ст'),
                                                     ('3', '3ст'),
                                                     ('cd', 'Сd'),
                                                     ('empty', 'empty'),))


class VEU(JournalTable):
    hot = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    cold = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    comment = models.CharField(max_length=128, blank=True)


class Sample2(JournalTable):
    cd = models.DecimalField(max_digits=10, decimal_places=5, blank=True)
    cu = models.DecimalField(max_digits=10, decimal_places=5, blank=True)


class FreeTank(JournalTable):
    str_num = models.DecimalField(max_digits=2, decimal_places=0, blank=False)
    tank_name = models.CharField(max_length=128, blank=True, null=True)
    prev_measure = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    cur_measure = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    deviation = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)


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