# Generated by Django 2.1 on 2018-09-19 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modes', '0003_auto_20180919_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mode',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
