# Generated by Django 2.1.3 on 2018-11-29 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('all_journals_app', '0012_auto_20181128_1623'),
        ('dictionaries', '0002_auto_20181113_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipmentdict',
            name='plant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='all_journals_app.Plant'),
            preserve_default=False,
        ),
    ]
