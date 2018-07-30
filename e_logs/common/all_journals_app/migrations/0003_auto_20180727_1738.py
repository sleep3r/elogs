# Generated by Django 2.0.6 on 2018-07-27 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('all_journals_app', '0002_cell_responsible'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cell',
            name='comment',
            field=models.CharField(max_length=1024, null=True, verbose_name='Комментарий к ячейке'),
        ),
        migrations.AlterField(
            model_name='cell',
            name='index',
            field=models.IntegerField(default=None, verbose_name='Номер строчки'),
        ),
        migrations.AlterField(
            model_name='cell',
            name='value',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='Значение поля'),
        ),
    ]
