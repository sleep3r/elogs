from django.db import models

class Setting(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название')
    value = models.CharField(max_length=2048, verbose_name='Значение')
    plant = models.CharField(max_length=128, verbose_name='Цех', blank=True, null=True)
    journal = models.CharField(max_length=128, verbose_name='Журнал', blank=True, null=True)
    table = models.CharField(max_length=128, verbose_name='Таблица', blank=True, null=True)
    cell = models.CharField(max_length=128, verbose_name='Ячейка', blank=True, null=True)

    @staticmethod
    def get_setting_value(name, plant=None, journal=None, table=None, cell=None):
        settings = Setting.objects.filter(name=name)
        if cell is not None:
            cell_settings = settings.filter(cell=cell)
            if cell_settings.count() > 0:
                return cell_settings[0].value

        if table is None and journal is None and plant is None:
            tables = Setting.objects.exclude(table__isnull=True).filter(name=name)
            if tables.count() > 0:
                table = tables[0].table
            else:
                table = None

        if table is not None:
            table_settings = settings.filter(table=table)
            if table_settings.count() > 0:
                return table_settings[0].value

        if journal is None and plant is None:
            journals = Setting.objects.exclude(journal__isnull=True).filter(name=name)
            if journals.count() > 0:
                journal = journals[0].journal
            else:
                journal = None

        if journal is not None:
            journal_settings = settings.filter(journal=journal)
            if journal_settings.count() > 0:
                return journal_settings[0].value

        if plant is None:
            plants = Setting.objects.exclude(plant__isnull=True).filter(name=name)
            if plants.count() > 0:
                plant = plants[0].plant
            else:
                plant = None

        if plant is not None:
            plant_settings = settings.filter(plant=plant)
            if plant_settings.count() > 0:
                return plant_settings[0].value

        raise ValueError("No setting for such scope")