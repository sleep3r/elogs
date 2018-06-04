import time
from django.contrib.auth.models import User
from django.db import models


class Shift:  # TODO: add everywhere links to
    order = models.DecimalField(max_digits=1)
    master = models.CharField(max_length=50)
    laborant = models.CharField(max_length=50)


# Low Sink High Sink
class LSUSAnal:
    time = models.DateTimeField()
    point = models.CharField(max_length=1, choices=(('0', 'lshs'),
                                                    ('1', 'larox'),
                                                    ('2', 'purified'),
                                                    ('3', 'errors'),))

    co = models.DecimalField(max_digits=6)
    sb = models.DecimalField(max_digits=6)
    cu = models.DecimalField(max_digits=6)
    cu_st1 = models.DecimalField(max_digits=6)
    cd = models.DecimalField(max_digits=6)
    solid_st1 = models.DecimalField(max_digits=6)
    ph = models.DecimalField(max_digits=6)
    fe = models.DecimalField(max_digits=6)
    macenic = models.DecimalField(max_digits=6)
    solid = models.DecimalField(max_digits=6)
    density = models.DecimalField(max_digits=6)
    current = models.DecimalField(max_digits=6)

    norm = models.DecimalField(max_digits=6)
    fact = models.DecimalField(max_digits=6)


class DenserAnal:
    time = models.DateTimeField()
    point = models.CharField(max_length=1, choices=(('0', '10'),
                                                    ('1', '11'),
                                                    ('2', '12'),))

    sink = models.CharField(max_length=1, choices=(('0', 'upper'),
                                                    ('1', 'lower')))
    ph = models.DecimalField(max_digits=6)
    cu = models.DecimalField(max_digits=6)
    fe = models.DecimalField(max_digits=6)
    liq_sol = models.DecimalField(max_digits=6)


class ZnPulpAnal:
    time = models.DateTimeField()
    liq_sol = models.DecimalField(max_digits=6)
    ph = models.DecimalField(max_digits=6)
    t0 = models.DecimalField(max_digits=6)


class CuPulpAnal:
    time = models.DateTimeField()
    liq_sol = models.DecimalField(max_digits=6)
    before = models.DecimalField(max_digits=6)
    after = models.DecimalField(max_digits=6)
    tv = models.DecimalField(max_digits=6)  # TODO: WHF??


class FeSolutionAnal:
    time = models.DateTimeField()
    h2so4 = models.DecimalField(max_digits=6)
    sb = models.DecimalField(max_digits=6)  # TODO: WHF??
    cu = models.DecimalField(max_digits=6)
    fe = models.DecimalField(max_digits=6)
    density = models.DecimalField(max_digits=6)


class DailyAnalysis:  # TODO: WHF??
    time = models.DateTimeField()
    shlippe_sb = models.DecimalField(max_digits=6)
    activ_sas = models.DecimalField(max_digits=6)  # SAS is how american shitheads call ПАВ
    circulation_denser = models.DecimalField(max_digits=6)
    fe = models.DecimalField(max_digits=6)
    density = models.DecimalField(max_digits=6)


class FeSolutionAnal:
    time = models.DateTimeField()
    h2so4 = models.DecimalField(max_digits=6)
    sb = models.DecimalField(max_digits=6)  # TODO: WHF??
    cu = models.DecimalField(max_digits=6)
    fe = models.DecimalField(max_digits=6)
    density = models.DecimalField(max_digits=6)


# -----------------------------------------------------

class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)
    shortcut = models.CharField(max_length=5, unique=True)

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]

class Conference(models.Model):
    name = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    languages = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=6, choices=(('open',)*2, ('closed',)*2))
    recognition = models.CharField(max_length=3, choices=(('in',)*2, ('out',)*2))
    state = models.CharField(max_length=6, choices=(('past',)*2, ('active',)*2, ('future',)*2))
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    talkers_changed = models.ManyToManyField('Talker', related_name='new_in_conf')
    recog_counter = models.FloatField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        permissions = (
            ('can_room', 'Может редактировать комнату.'),
            ('can_manage', 'Может редактировать пользователей.'),
            ('can_open', 'Может открыть закрытую конференцию.'),
            ('can_admin', 'Может может назначать начальников отдела и права.'),
        )


def get_rus_lang():
    return Language.objects.get(shortcut='ru').id


class Talker(models.Model):
    name = models.CharField(max_length=127)
    title = models.CharField(max_length=127)
    email = models.EmailField()
    line = models.IntegerField()
    lastcompiled = models.DateTimeField(null=True)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, null=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('conference', 'line')
        ordering = ["name"]


class Track(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    talker = models.ForeignKey(Talker, on_delete=models.CASCADE)
    offset = models.BigIntegerField()
    duration = models.IntegerField()
    path = models.CharField(max_length=255, unique=True)
    text = models.TextField()
    is_active = models.BooleanField(default=True)
    cut = models.BooleanField(default=False)

    class Meta:
        ordering = ["conference", "offset"]


def get_time():
    return int(float(time.time()))


class TrackQueue(models.Model):
    conference = models.ForeignKey(Conference, null=True)
    queue = models.TextField(default='{}', blank=False)
    last_refresh = models.IntegerField(default=get_time)
    is_active = models.BooleanField(default=True, blank=False)


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    csrf = models.CharField(max_length=CSRF_LENGTH, default='')
