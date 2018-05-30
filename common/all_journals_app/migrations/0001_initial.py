# Generated by Django 2.0.4 on 2018-05-16 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CellValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_name', models.CharField(max_length=128, verbose_name='Название таблицы')),
                ('field_name', models.CharField(max_length=128, verbose_name='Название поля')),
                ('index', models.IntegerField(blank=True, default=None, null=True, verbose_name='Номер строчки')),
                ('value', models.CharField(max_length=1024, verbose_name='Минимальный размер')),
            ],
        ),
        migrations.CreateModel(
            name='JournalPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('shift', 'Смена'), ('equipment', 'Оборудование'), ('month', 'Месяц')], max_length=128)),
                ('journal_name', models.CharField(max_length=256, verbose_name='Название журнала')),
            ],
        ),
        migrations.AddField(
            model_name='cellvalue',
            name='journal_page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='all_journals_app.JournalPage'),
        ),
    ]