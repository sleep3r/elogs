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