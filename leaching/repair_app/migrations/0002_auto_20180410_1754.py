# Generated by Django 2.0.3 on 2018-04-10 14:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repair_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Repairs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='Время анализа/создания записи')),
                ('date', models.DateTimeField(verbose_name='Дата осмотра')),
                ('name', models.CharField(blank=True, max_length=1024, verbose_name='Наименование узла и характеристика дефектов')),
                ('comment', models.CharField(blank=True, max_length=1024, verbose_name='Дата и объем выполненных работ по устранению неисправностей')),
            ],
        ),
        migrations.DeleteModel(
            name='CuPulpAnal',
        ),
    ]