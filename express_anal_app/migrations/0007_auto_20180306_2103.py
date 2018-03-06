# Generated by Django 2.0.2 on 2018-03-06 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('express_anal_app', '0006_auto_20180306_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='denseranal',
            name='cu',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True, verbose_name='Cu'),
        ),
        migrations.AlterField(
            model_name='denseranal',
            name='fe',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True, verbose_name='Fe'),
        ),
        migrations.AlterField(
            model_name='denseranal',
            name='liq_sol',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True, verbose_name='Ж:Т'),
        ),
        migrations.AlterField(
            model_name='denseranal',
            name='ph',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True, verbose_name='pH'),
        ),
        migrations.AlterField(
            model_name='leachingexpressanal',
            name='arsenic',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True, verbose_name='As'),
        ),
        migrations.AlterField(
            model_name='leachingexpressanal',
            name='cd',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True, verbose_name='Cd'),
        ),
        migrations.AlterField(
            model_name='leachingexpressanal',
            name='co',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True, verbose_name='Co'),
        ),
        migrations.AlterField(
            model_name='leachingexpressanal',
            name='cu',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True, verbose_name='Cu'),
        ),
        migrations.AlterField(
            model_name='leachingexpressanal',
            name='cu_st1',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True, verbose_name='Cu ст.1'),
        ),
        migrations.AlterField(
            model_name='leachingexpressanal',
            name='current',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True, verbose_name='Выход по току'),
        ),
        migrations.AlterField(
            model_name='leachingexpressanal',
            name='density',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True, verbose_name='Уд. вес'),
        ),
        migrations.AlterField(
            model_name='leachingexpressanal',
            name='fe',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True, verbose_name='Fe'),
        ),
        migrations.AlterField(
            model_name='leachingexpressanal',
            name='ph',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True, verbose_name='pH'),
        ),
        migrations.AlterField(
            model_name='leachingexpressanal',
            name='sb',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True, verbose_name='Sb'),
        ),
        migrations.AlterField(
            model_name='leachingexpressanal',
            name='solid',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True, verbose_name='Твердое г\\л'),
        ),
        migrations.AlterField(
            model_name='leachingexpressanal',
            name='solid_st1',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True, verbose_name='Cd'),
        ),
        migrations.AlterField(
            model_name='productionerrors',
            name='error',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True, verbose_name='Несоответствие'),
        ),
        migrations.AlterField(
            model_name='productionerrors',
            name='fact',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True, verbose_name='Факт'),
        ),
        migrations.AlterField(
            model_name='productionerrors',
            name='norm',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True, verbose_name='Норма'),
        ),
    ]
