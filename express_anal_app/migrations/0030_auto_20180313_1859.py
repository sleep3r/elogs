# Generated by Django 2.0.2 on 2018-03-13 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('express_anal_app', '0029_auto_20180313_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='electrolysis',
            name='loads1',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=1, null=True),
        ),
        migrations.AlterField(
            model_name='electrolysis',
            name='loads2',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=1, null=True),
        ),
    ]