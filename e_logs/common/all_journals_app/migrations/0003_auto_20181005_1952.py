# Generated by Django 2.1 on 2018-10-05 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('all_journals_app', '0002_auto_20181002_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='field',
            name='verbose_name',
            field=models.CharField(default='', max_length=256, verbose_name='Название столбца'),
            preserve_default=False,
        ),
    ]
