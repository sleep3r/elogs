from django.db import models



class ConcentrateDict(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name = 'Концентрат'
        verbose_name_plural = 'Концентраты'


class EquipmentDict(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'