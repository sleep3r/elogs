# Generated by Django 2.1 on 2018-09-14 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('all_journals_app', '0008_auto_20180911_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='shift',
            name='ended',
            field=models.BooleanField(default=False),
        ),
    ]
