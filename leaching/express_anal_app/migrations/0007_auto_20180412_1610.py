# Generated by Django 2.0.3 on 2018-04-12 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('express_anal_app', '0006_remove_shift_plant'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shift',
            options={'ordering': ['date', 'order']},
        ),
    ]
