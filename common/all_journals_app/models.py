from django.db import models


class JournalPage(models.Model):
    type = models.CharField(max_length=128, choices=(('shift', 'Смена'),
                                                     ('equipment', 'Оборудование'),
                                                     ('month', 'Месяц')))
    journal_name = models.CharField(max_length=256, verbose_name='Название журнала')


class CellValue(models.Model):
    journal_page = models.ForeignKey(JournalPage, on_delete=models.CASCADE)
    table_name = models.CharField(max_length=128, verbose_name='Название таблицы')
    field_name = models.CharField(max_length=128, verbose_name='Название поля')
    index = models.IntegerField(null=True, blank=True, default=None, verbose_name='Номер строчки')

    value = models.CharField(max_length=1024, verbose_name='Значение поля')

    class Meta:
        unique_together = ('journal_page', 'table_name', 'field_name', 'index')

    def __str__(self):
        return "journal_page: " + str(self.journal_page) + " table_name: " \
               + str(self.table_name) + " field_name: " + str(self.field_name) +\
               " index: " + str(self.index) + " value: " + str(self.value)
