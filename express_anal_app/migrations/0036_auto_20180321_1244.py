# Generated by Django 2.0.2 on 2018-03-21 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('express_anal_app', '0035_auto_20180315_1958'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProductionErrors',
            new_name='ProductionError',
        ),
    ]