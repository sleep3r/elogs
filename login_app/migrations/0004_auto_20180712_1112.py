# Generated by Django 2.0.7 on 2018-07-12 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0003_employee_owned_journal_pages'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='addressee',
        ),
        migrations.AlterModelOptions(
            name='employee',
            options={'verbose_name': 'Рабочий', 'verbose_name_plural': 'Рабочие'},
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]