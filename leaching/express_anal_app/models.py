import datetime
import time

from decimal import Decimal
from django.contrib.auth.models import User
from django.db import models

from login_app.models import Employee


class Journal(models.Model):
    """
    Модель производственного журнала. Содержит название журнала и его описание.
    """
    name = models.CharField(max_length=1000, blank=False, null=False, verbose_name='Название журнала')
    description = models.TextField(verbose_name='Описание таблицы')
    plant = models.CharField(max_length=10, verbose_name='Цех', choices=(('furnace', 'обжиг'),
                                                                         ('leaching', 'выщелачивание'),
                                                                         ('electrolysis', 'электролиз'),))

    def __str__(self):
        return self.name


class Shift(models.Model):
    """
    Модель смены завода. Содержит основные данные такие как дата, номер смены, цех и основные сутрудники смены.
    """
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
    """
    Базовая модель для всех моделей, хранящих данные журналов. Содержит ссылку на смену и на журнал.
    """
    shift = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Смена')
    time = models.DateTimeField(verbose_name='Время анализа/создания записи', default=datetime.datetime.now)
    journal = models.ForeignKey(Journal, on_delete=models.SET_NULL, null=True, verbose_name='Журнал')

    def __str__(self):
        return f'{self.journal}, запись {self.time}'


class LeachingExpressAnal(JournalTable):
    """
    Модель хранит данные, которые отображаются в верхней таблице, кроме секции с управлением продукцией
    Каждая строчка в базе данных представляет из себя одну секцию в таблице (ВСНС, Ларокс, Очищенный раствор),
    при этом заполняются только те поля, которые есть в данной секции, остальные поля остаются пустыми.
    Сама секция хранится в поле point
    """
    point = models.CharField(max_length=20, verbose_name='Место измерения', choices=(('lshs','ВСНС'),
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


class ProductionError(JournalTable):
    """
    Эта модель хранит 1 строчку последней секции верхней таблицы. Данные последних трех столбцов дублируются в каждой записи.
    """
    norm = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='Норма')
    fact = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='Факт')
    error = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='Несоответствие')
    correction = models.CharField(max_length=512, verbose_name='Коррекция', blank=True, null=True)
    verified = models.BooleanField(default=False, verbose_name='Проверено', blank=True )


class DenserAnal(JournalTable):
    """
    Эта модель хранит данные по таблице сгустителей. Заполняются только те поля, которые присутствуют в данной секции.
    Секцией является уникальная комбинация слива и сгустителя. Для каждой секциии и времени
    в базе содержится ровно одна запись.
    """
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
    """
    Эта модель хранит данные по 1 строчке первой секции таблицы пульп.
    """
    liq_sol = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='Ж:Т')
    ph = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='pH')
    t0 = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='t0')


class CuPulpAnal(JournalTable):
    """
    Эта модель хранит данные по 1 строчке второй секции таблицы пульп.
    """
    liq_sol = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='Ж:Т')
    before = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='До')
    after = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='После')
    solid = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='ТВ')

    zn_pulp_anal = models.OneToOneField(ZnPulpAnal, on_delete=models.CASCADE,
                                        related_name='cu_pulp_anal')


class FeSolutionAnal(JournalTable):
    """
    Эта модель хранит данные по 1 строчке третьей секции таблицы пульп.
    """
    h2so4 = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='H2SO4')
    solid = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='ТВ')
    sb = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='Sb')
    cu = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='Cu')
    fe = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='Fe')
    density = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='Уд. вес')
    arsenic = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='As')
    cl = models.DecimalField(max_digits=10, decimal_places=5, blank=True, verbose_name='Cl')

    cu_pulp_anal = models.OneToOneField(CuPulpAnal, on_delete=models.CASCADE, related_name='fe_solution_anal')
    zn_pulp_anal = models.OneToOneField(ZnPulpAnal, on_delete=models.CASCADE, related_name='fe_solution_anal')


class DailyAnalysis(JournalTable):
    """
    Эта модель хранит данные по последней секции таблицы пульп. Там где активность пав и все остальное.
    Есть тольк одна запись на таблицу.
    """
    shlippe_sb = models.CharField(max_length=64, blank=True, verbose_name='Концентрация Sb в р-ре соли Шлиппе')
    activ_sas = models.CharField(max_length=64, blank=True, verbose_name='Активность ПАВ')
    circulation_denser = models.CharField(max_length=64, blank=True, verbose_name='Анализы оборот. сгуст.')
    fe_hi1 = models.CharField(max_length=64, blank=True, verbose_name='Высоко Fe р-р')
    fe_hi2 = models.CharField(max_length=64, blank=True, verbose_name='Высоко Fe р-р 2')


class HydroMetal(JournalTable):
    """
    Хранит 1 строчку из таблицы гидрометаллург 1
    """
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
    """
    Хранит нижнюю часть таблицы гидрометаллург 1. Одиночные поля копируются в каждой записи.
    Одна запись соответствует одному измерению гранулярности.
    """
    gran = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='Ситовой огарка')
    gran_avg = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True,
                                   verbose_name='Ситовой огарка средний')
    fe_avg = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True,
                                 verbose_name='Общее Fe среднее')
    fe_shave = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, verbose_name='Fe Стружка Fe')

    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL,
                                 null=True, verbose_name='Аппаратчик-гидрометаллург')


class Agitators(JournalTable):
    """
    Модель хранит 1 строчку, одного агитатора в одном состоянии (до/после) в таблице гидрометаллургов.
    """
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
    """
    Модель хранит 1 столбец таблицы нейтральных сгустителей.
    """
    num = models.DecimalField(max_digits=2, decimal_places=0)
    sediment = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    liq_sol1 = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    liq_sol2 = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)


class ReadyProduct(JournalTable):
    """
    Модель хранит 1 строчку таблицы баков готовой продукции
    """
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


class Reagents(JournalTable):
    """
    Модель хранит столбцы таблицы Реагенты.<br>
    state Тип столбца (Доставлено, принято, ...).<br>
    Если тип столбца не none, то stage должно быть ='total'<br>
    Есть особое значение state=none. В записях state=none хранятся только поля<br>
    stage которые означают поле внутренней таблицы и поле zn_dust.<br>
    Поле fence_sate дублируется в каждом столбце.<br>
    Такие дела...
    """
    shlippe = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    zn_dust = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    mg_ore = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    magnaglobe = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    fe_shave = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)

    state = models.CharField(max_length=20, choices=(('delivered', 'Доставлено'),
                                                     ('taken', 'Принято'),
                                                     ('consumption', 'Расход'),
                                                     ('issued', 'Сдано'),
                                                     ('none', 'Для стадий'),))

    stage = models.CharField(max_length=20, default='total', choices=(('1st', '1ст'),
                                                     ('2st', '2ст'),
                                                     ('3st', '3ст'),
                                                     ('cd', 'Cd'),
                                                     ('total', 'Всего'),))

    fence_state = models.CharField(max_length=255, blank=True)


class VEU(JournalTable):
    """
    Одна строка таблицы VEU
    """
    num = models.DecimalField(max_digits=1, decimal_places=0, blank=True, null=True)
    hot = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    cold = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    comment = models.CharField(max_length=128, blank=True, null=True)


class Sample2(JournalTable):
    """
    Одна строка таблицы Пробник номер 2
    """
    cd = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    cu = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)


class FreeTank(JournalTable):
    """
    Одна строка таблицы Пробник номер 2
    """
    str_num = models.DecimalField(max_digits=2, decimal_places=0, blank=False)
    tank_name = models.CharField(max_length=128, blank=True, null=True)
    prev_measure = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    cur_measure = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    deviation = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)


class SelfSecurity(JournalTable):
    """
    Одна строка таблицы самоохрана
    Поле bignote дублируется в каждой строке
    """
    note = models.CharField(max_length=64, blank=True)
    bignote = models.CharField(max_length=256, blank=True)


class Electrolysis(JournalTable):
    """
    Содержит один столбец таблицы электролиза. Поле series содержит серию.
    Отсутствующие значения не выставляются.
    Поле comment дублируется в каждом столбце.
    Добавлены два значения для времени в каждый столбец.
    """
    series = models.DecimalField(max_digits=3, decimal_places=0)
    loads1 = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    loads2 = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    time1 = models.DateTimeField(blank=True, null=True)
    time2 = models.DateTimeField(blank=True, null=True)
    counter = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    bunkers_weltz = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    silos_furnace = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    bunkers_furnace = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    comment = models.CharField(max_length=256, blank=True)


class ShiftInfo(JournalTable):
    """
    Модель содержит всю информацибю по объекту смены.
    """
    out_sol_t = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    out_sol_c = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    out_pulp_cvck = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # TODO: fuck!
    out_cu_kek = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    out_cd_sponge = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    out_electr = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    out_ruch_cd = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    out_neutr = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    out_cu_pulp = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)

    in_filtrate_ls = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    in_filtrate_dens = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    in_fe = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    in_fe_hi = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    in_poor_cd = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)

    this_master = models.ForeignKey(Employee, on_delete=models.SET_NULL,
                                    null=True, related_name='handed_over_shift_info',
                                    blank=True, verbose_name='Мастер сдал',)
    next_master = models.ForeignKey(Employee, on_delete=models.SET_NULL,
                                    null=True, related_name='taken_shift_info',
                                    blank=True, verbose_name='Мастер принял')
    furnaces = models.CharField(max_length=3, blank=True)

    free_13 = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    free_14 = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    free_13_t = models.CharField(max_length=10, blank=True)
    free_14_t = models.CharField(max_length=10, blank=True)


class Schieht(JournalTable):
    """
    Модель 1 строку таблицы шихты.
    """
    num = models.DecimalField(max_digits=2, decimal_places=0)
    name = models.CharField(max_length=64, blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)


class NeutralSolution(JournalTable):
    """
    Модель содержит один столбец таблицы нейтральных растворов.
    """
    str_num = models.DecimalField(max_digits=2, decimal_places=0, blank=False)
    tank_name = models.CharField(max_length=40, blank=False)
    value = models.DecimalField(max_digits=10, decimal_places=5, blank=True)


class Cinder(JournalTable):
    """
    Модель содержит одну строку таблицы ограка.
    """
    col_num = models.DecimalField(max_digits=1, decimal_places=0, blank=False)
    shift_total = models.DecimalField(max_digits=15, decimal_places=5, blank=True)
    day_total = models.DecimalField(max_digits=15, decimal_places=5, blank=True)
    in_process = models.DecimalField(max_digits=15, decimal_places=5, blank=True)