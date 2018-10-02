# Generated by Django 2.1 on 2018-10-02 15:07

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('all_journals_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FieldConstraints',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_normal', models.IntegerField()),
                ('max_normal', models.IntegerField()),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='all_journals_app.Field')),
            ],
            options={
                'verbose_name': 'Ограничения для поля',
                'verbose_name_plural': 'Ограничения для полей',
            },
        ),
        migrations.CreateModel(
            name='Mode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False)),
                ('message', models.CharField(default='', max_length=512)),
                ('beginning', models.DateTimeField(default=django.utils.timezone.now)),
                ('end', models.DateTimeField(null=True)),
                ('journal', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='all_journals_app.Journal')),
            ],
            options={
                'verbose_name': 'Режим',
                'verbose_name_plural': 'Режимы',
            },
        ),
        migrations.AddField(
            model_name='fieldconstraints',
            name='mode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modes.Mode'),
        ),
    ]
