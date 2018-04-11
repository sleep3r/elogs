from django.db import models
from django.utils import timezone

from furnace.fractional_app.servises.constants import SCHIEHT_SIZES, CINDER_SIZES
from utils.errors import SemanticError


class Measurement(models.Model):
    auto_time = models.DateTimeField(verbose_name='Время создания записи', default=timezone.now)
    user_time = models.DateTimeField(verbose_name='Время анализа', null=True, blank=True)

    def add(self, masses, sizes, time):
        self.user_time = time
        self.save()
        for m, s in zip(masses, sizes):
            w = Weight(mass=m, min_size=s, measurement=self)
            w.save()

        return self


class SchiehtMeasurement(Measurement):
    """
    Одно измерение гранулярного состава шихты
    """
    def __str__(self):
        return f'[{self.auto_time}] измерение шихты'


class CinderMeasurement(Measurement):
    """
    Одно измерение гранулярного состава огарка
    """
    def __str__(self):
        return f'[{self.auto_time}] измерение огарка'


class Weight(models.Model):
    mass = models.FloatField(null=True, blank=True, verbose_name='Масса')
    min_size = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Минимальный размер')
    measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE, related_name='weights')

    class Meta:
        ordering = ['min_size']


class MeasurementPair(models.Model):
    cinder = models.OneToOneField(CinderMeasurement, on_delete=models.SET_NULL, null=True, related_name='pair')
    schieht = models.OneToOneField(SchiehtMeasurement, on_delete=models.SET_NULL, null=True, related_name='pair')

    def add_weights(self, schiehts, cinder, stime, ctime):
        self.cinder = CinderMeasurement().add(cinder, CINDER_SIZES, ctime)
        self.schieht = SchiehtMeasurement().add(schiehts, SCHIEHT_SIZES, stime)
        self.save()

        return self
