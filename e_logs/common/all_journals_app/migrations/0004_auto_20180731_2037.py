# Generated by Django 2.0.6 on 2018-07-31 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('all_journals_app', '0003_auto_20180731_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cell',
            name='group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='all_journals_app.CellGroup'),
            preserve_default=False,
        ),
    ]
