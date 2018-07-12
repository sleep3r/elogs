# Generated by Django 2.0.7 on 2018-07-12 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login_app', '0004_auto_20180712_1112'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_read', models.BooleanField(default=False, verbose_name='Прочитано')),
                ('text', models.TextField(verbose_name='Текст сообщения')),
                ('type', models.CharField(choices=[('critical_value', 'Критическое значение'), ('comment', 'Замечание')], max_length=100, null=True, verbose_name='Тип сообщения')),
                ('cell_field_name', models.CharField(default=None, max_length=128, null=True, verbose_name='Название поля ячейки')),
                ('cell_table_name', models.CharField(default=None, max_length=128, null=True, verbose_name='Название таблицы ячейки')),
                ('cell_journal_page', models.IntegerField(blank=True, default=None, null=True, verbose_name='Номер журнала ячейки')),
                ('row_index', models.IntegerField(blank=True, default=None, null=True, verbose_name='Номер строчки ячейки')),
                ('addressee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='messages', to='login_app.Employee')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
            },
        ),
    ]
