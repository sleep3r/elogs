# Generated by Django 2.0.2 on 2018-03-12 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('express_anal_app', '0019_merge_20180312_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample2',
            name='cd',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='sample2',
            name='cu',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='veu',
            name='cold',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='veu',
            name='comment',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='veu',
            name='hot',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True),
        ),
    ]
