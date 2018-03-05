# Generated by Django 2.0.2 on 2018-03-05 08:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('position', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='JournalTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.DecimalField(decimal_places=0, max_digits=1)),
                ('plant', models.CharField(choices=[('0', 'furnace'), ('1', 'leaching'), ('2', 'electrolysis')], max_length=1)),
                ('laborant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leaching_shift_labornats', to='express_anal_app.Employee')),
                ('master', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leaching_shift_masters', to='express_anal_app.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='Agitators',
            fields=[
                ('journaltable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='express_anal_app.JournalTable')),
                ('before', models.BooleanField()),
                ('ph', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('cu', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('co', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('cd', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('h2so4', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('comment', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='express_anal_app.Employee')),
            ],
            bases=('express_anal_app.journaltable',),
        ),
        migrations.CreateModel(
            name='CinderDensity',
            fields=[
                ('journaltable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='express_anal_app.JournalTable')),
                ('gran', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('gran_avg', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('fe_avg', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('fe_shave', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='express_anal_app.Employee')),
            ],
            bases=('express_anal_app.journaltable',),
        ),
        migrations.CreateModel(
            name='CuPulpAnal',
            fields=[
                ('journaltable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='express_anal_app.JournalTable')),
                ('liq_sol', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('before', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('after', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('solid', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
            ],
            bases=('express_anal_app.journaltable',),
        ),
        migrations.CreateModel(
            name='DailyAnalysis',
            fields=[
                ('journaltable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='express_anal_app.JournalTable')),
                ('shlippe_sb', models.CharField(blank=True, max_length=64)),
                ('activ_sas', models.CharField(blank=True, max_length=64)),
                ('circulation_denser', models.CharField(blank=True, max_length=64)),
                ('fe_hi1', models.CharField(blank=True, max_length=64)),
                ('fe_hi2', models.CharField(blank=True, max_length=64)),
            ],
            bases=('express_anal_app.journaltable',),
        ),
        migrations.CreateModel(
            name='DenserAnal',
            fields=[
                ('journaltable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='express_anal_app.JournalTable')),
                ('point', models.CharField(choices=[('0', '10'), ('1', '11'), ('2', '12')], max_length=1)),
                ('sink', models.CharField(choices=[('0', 'upper'), ('1', 'lower')], max_length=1)),
                ('ph', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('cu', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('fe', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('liq_sol', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
            ],
            bases=('express_anal_app.journaltable',),
        ),
        migrations.CreateModel(
            name='Electrolysis',
            fields=[
                ('journaltable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='express_anal_app.JournalTable')),
                ('series', models.DateTimeField()),
                ('loads1', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('loads2', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('counter', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('bunkers_weltz', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('silos_furnace', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('bunkers_furnace', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
            ],
            bases=('express_anal_app.journaltable',),
        ),
        migrations.CreateModel(
            name='FeSolutionAnal',
            fields=[
                ('journaltable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='express_anal_app.JournalTable')),
                ('h2so4', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('solid', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('sb', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('cu', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('fe', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('density', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('As', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('Cl', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
            ],
            bases=('express_anal_app.journaltable',),
        ),
        migrations.CreateModel(
            name='FreeTank',
            fields=[
                ('journaltable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='express_anal_app.JournalTable')),
                ('tank_name', models.CharField(blank=True, max_length=128)),
                ('prev_measure', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('deviation', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
            ],
            bases=('express_anal_app.journaltable',),
        ),
        migrations.CreateModel(
            name='HydroMetal',
            fields=[
                ('journaltable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='express_anal_app.JournalTable')),
                ('ph', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('acid', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('fe2', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('fe_total', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('cu', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('sb', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('sediment', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('mann_num', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='express_anal_app.Employee')),
            ],
            bases=('express_anal_app.journaltable',),
        ),
        migrations.CreateModel(
            name='LeachingExpressAnal',
            fields=[
                ('journaltable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='express_anal_app.JournalTable')),
                ('point', models.CharField(choices=[('0', 'lshs'), ('1', 'larox'), ('2', 'purified'), ('3', 'errors')], max_length=1)),
                ('co', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('sb', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('cu', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('cu_st1', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('cd', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('solid_st1', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('ph', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('fe', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('arsenic', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('solid', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('density', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('current', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
            ],
            bases=('express_anal_app.journaltable',),
        ),
        migrations.CreateModel(
            name='NeutralDenser',
            fields=[
                ('journaltable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='express_anal_app.JournalTable')),
                ('num', models.DateTimeField()),
                ('sediment', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('liq_sol1', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('liq_sol2', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
            ],
            bases=('express_anal_app.journaltable',),
        ),
        migrations.CreateModel(
            name='NeutralSolution',
            fields=[
                ('journaltable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='express_anal_app.JournalTable')),
                ('tank_name', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('value', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
            ],
            bases=('express_anal_app.journaltable',),
        ),
        migrations.CreateModel(
            name='ProductionErrors',
            fields=[
                ('journaltable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='express_anal_app.JournalTable')),
                ('norm', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('fact', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('error', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('correction', models.CharField(max_length=512)),
                ('verified', models.BooleanField(default=False)),
            ],
            bases=('express_anal_app.journaltable',),
        ),
        migrations.CreateModel(
            name='ReadyProduct',
            fields=[
                ('journaltable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='express_anal_app.JournalTable')),
                ('num', models.DecimalField(blank=True, decimal_places=0, max_digits=1)),
                ('cd', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('cu', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('co', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('sb', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('fe', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('vt', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('density', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('norm', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('fact', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('correction', models.CharField(blank=True, max_length=128)),
                ('verified', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
            ],
            bases=('express_anal_app.journaltable',),
        ),
        migrations.CreateModel(
            name='Reagents',
            fields=[
                ('journaltable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='express_anal_app.JournalTable')),
                ('shlippe', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('zn', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('mg', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('magnaglobe', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('fe_shave', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('fence_state', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('delivered', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('accepted', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('consumption', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('taken_away', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('stage', models.CharField(choices=[('0', '1'), ('1', '2'), ('2', '3'), ('3', 'cd'), ('4', 'empty')], max_length=1)),
            ],
            bases=('express_anal_app.journaltable',),
        ),
        migrations.CreateModel(
            name='Sample2',
            fields=[
                ('journaltable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='express_anal_app.JournalTable')),
                ('cd', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('cu', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
            ],
            bases=('express_anal_app.journaltable',),
        ),
        migrations.CreateModel(
            name='Schieht',
            fields=[
                ('journaltable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='express_anal_app.JournalTable')),
                ('num', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('name', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('value', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
            ],
            bases=('express_anal_app.journaltable',),
        ),
        migrations.CreateModel(
            name='SelfSecurity',
            fields=[
                ('journaltable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='express_anal_app.JournalTable')),
                ('note', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('bignote', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
            ],
            bases=('express_anal_app.journaltable',),
        ),
        migrations.CreateModel(
            name='ShiftInfo',
            fields=[
                ('journaltable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='express_anal_app.JournalTable')),
                ('out_sol_t', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('out_sol_c', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('out_pulp_cvck', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('out_cu_kek', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('out_cd_sponge', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('out_electr', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('out_ruch_cd', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('out_neutr', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('out_cu_pulp', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('in_filtrate_ls', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('in_filtrate_dens', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('in_fe', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('in_fe_hi', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('in_poor_cd', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
            ],
            bases=('express_anal_app.journaltable',),
        ),
        migrations.CreateModel(
            name='VIU',
            fields=[
                ('journaltable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='express_anal_app.JournalTable')),
                ('hot', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('cold', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('comment', models.CharField(blank=True, max_length=128)),
            ],
            bases=('express_anal_app.journaltable',),
        ),
        migrations.CreateModel(
            name='ZnPulpAnal',
            fields=[
                ('journaltable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='express_anal_app.JournalTable')),
                ('liq_sol', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('ph', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
                ('t0', models.DecimalField(blank=True, decimal_places=5, max_digits=10)),
            ],
            bases=('express_anal_app.journaltable',),
        ),
        migrations.AddField(
            model_name='journaltable',
            name='journal',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='express_anal_app.Journal'),
        ),
        migrations.AddField(
            model_name='journaltable',
            name='shift',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='express_anal_app.Shift'),
        ),
    ]
