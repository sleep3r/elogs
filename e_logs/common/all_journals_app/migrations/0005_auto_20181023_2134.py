# Generated by Django 2.1.2 on 2018-10-23 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('all_journals_app', '0004_auto_20181023_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='field',
            name='type',
            field=models.CharField(default='', max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='field',
            name='units',
            field=models.CharField(default='', max_length=128, null=True),
        ),
    ]
