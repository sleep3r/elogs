from django.db import models



class ConcentrateDict(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        verbose_name = 'Концентрат'
        verbose_name_plural = 'Концентраты'


class EquipmentDict(models.Model):
    name = models.CharField(max_length=256)
    plant = models.ForeignKey('all_journals_app.Plant', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'