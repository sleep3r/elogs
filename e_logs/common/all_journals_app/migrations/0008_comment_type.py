# Generated by Django 2.1.3 on 2018-11-19 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('all_journals_app', '0007_month_month_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='type',
            field=models.CharField(choices=[('user_comment', 'Комментарий пользователя'), ('system_comment', 'Комментарий системы')], default='user_comment', max_length=32, verbose_name='Тип комментария'),
        ),
    ]
