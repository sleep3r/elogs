# Generated by Django 2.1.3 on 2018-11-06 14:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feedback',
            options={'verbose_name': 'Отзыв', 'verbose_name_plural': 'Отзывы'},
        ),
    ]
