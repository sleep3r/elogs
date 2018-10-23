# Generated by Django 2.1.2 on 2018-10-23 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0003_auto_20181023_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='position',
            field=models.CharField(blank=True, choices=[('master', 'Мастер смены'), ('hydro', 'Аппаратчик'), ('admin', 'Админ'), ('boss', 'Начальник цеха'), ('technologist', 'Технолог цеха'), ('senior technologist', 'Главный технолог'), ('senior master', 'Старший мастер'), ('plant master', 'Мастер цеха'), ('department director', 'Начальник отделения'), ('electrolysis duty', 'Дежурный по электролизу')], max_length=128, verbose_name='Должность'),
        ),
    ]
