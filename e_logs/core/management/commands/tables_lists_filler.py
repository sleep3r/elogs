from e_logs.common.all_journals_app.models import Plant, Journal
from e_logs.core.models import Setting


def fill_tables_lists():

    Setting.objects.bulk_create([
        Setting(
            scope=Journal.objects.get(
                plant=Plant.objects.get(name='furnace'),
                name='furnace_changed_fraction'
            ),
            name='tables_list',
            value='["tables/furnace/furnace_changed_fraction/main.html"]'
        ),
        Setting(
            scope=Journal.objects.get(
                plant=Plant.objects.get(name='furnace'),
                name='concentrate_report'
            ),
            name='tables_list',
            value='["tables/furnace/concentrate_report/small.html", "tables/furnace/concentrate_report/big.html", "tables/furnace/concentrate_report/lower_table.html(deleted)", "tables/furnace/concentrate_report/upper.html"]'
        ),
        Setting(
            scope=Journal.objects.get(
                plant=Plant.objects.get(name='furnace'),
                name='technological_tasks'
            ),
            name='tables_list',
            value='["tables/furnace/technological_tasks/main.html"]'
        ),
        Setting(
            scope=Journal.objects.get(
                plant=Plant.objects.get(name='furnace'),
                name='reports_furnace_area'
            ),
            name='tables_list',
            value='["tables/furnace/reports_furnace_area/main.html", "tables/furnace/reports_furnace_area/self_protection.html", "tables/furnace/reports_furnace_area/airmachines.html", "tables/furnace/reports_furnace_area/concentration_by_time.html", "tables/furnace/reports_furnace_area/fences.html", "tables/furnace/reports_furnace_area/worth.html", "tables/furnace/reports_furnace_area/electrofilter.html", "tables/furnace/reports_furnace_area/udel.html", "tables/furnace/reports_furnace_area/area_class_cinder.html", "tables/furnace/reports_furnace_area/warehouse_concentrates.html", "tables/furnace/reports_furnace_area/corrective_actions.html", "tables/furnace/reports_furnace_area/places_of_sampling.html"]'
        ),
        Setting(
            scope=Journal.objects.get(
                plant=Plant.objects.get(name='furnace'),
                name='furnace_repair'
            ),
            name='tables_list',
            value='["tables/furnace/furnace_repair/repair.html"]'
        ),
        Setting(
            scope=Journal.objects.get(
                plant=Plant.objects.get(name='furnace'),
                name='report_income_outcome_schieht'
            ),
            name='tables_list',
            value='["tables/furnace/report_income_outcome_schieht/supply_of_zinc_concentrates.html", "tables/furnace/report_income_outcome_schieht/main.html", "tables/furnace/report_income_outcome_schieht/small_plan.html", "tables/furnace/report_income_outcome_schieht/year_plan_schieht.html", "tables/furnace/report_income_outcome_schieht/summary.html"]'
        ),
        Setting(
            scope=Journal.objects.get(
                plant=Plant.objects.get(name='furnace'),
                name='metals_compute'
            ),
            name='tables_list',
            value='["tables/furnace/metals_compute/sgok.html", "tables/furnace/metals_compute/cinder_conc.html", "tables/furnace/metals_compute/main.html", "tables/furnace/metals_compute/contain_zn.html", "tables/furnace/metals_compute/concentrat.html", "tables/furnace/metals_compute/gof.html", "tables/furnace/metals_compute/sns.html", "tables/furnace/metals_compute/avg_month.html"]'
        ),
        Setting(
            scope=Journal.objects.get(
                plant=Plant.objects.get(name='furnace'),
                name='fractional'
            ),
            name='tables_list',
            value='[]'
        ),
        Setting(
            scope=Journal.objects.get(
                plant=Plant.objects.get(name='electrolysis'),
                name='masters_report'
            ),
            name='tables_list',
            value='["tables/electrolysis/masters_report/melt_area2.html", "tables/electrolysis/masters_report/zinc.html", "tables/electrolysis/masters_report/melt_area1.html", "tables/electrolysis/masters_report/seria1.html", "tables/electrolysis/masters_report/seria4.html", "tables/electrolysis/masters_report/seria3.html", "tables/electrolysis/masters_report/last.html", "tables/electrolysis/masters_report/params.html"]'
        ),
        Setting(
            scope=Journal.objects.get(
                plant=Plant.objects.get(name='electrolysis'),
                name='electrolysis_technical_report_3_degree'
            ),
            name='tables_list',
            value='["tables/electrolysis/electrolysis_technical_report_3_degree/right.html", "tables/electrolysis/electrolysis_technical_report_3_degree/left.html"]'
        ),
        Setting(
            scope=Journal.objects.get(
                plant=Plant.objects.get(name='electrolysis'),
                name='electrolysis_technical_report_4_degree'
            ),
            name='tables_list',
            value='["tables/electrolysis/electrolysis_technical_report_4_degree/right.html", "tables/electrolysis/electrolysis_technical_report_4_degree/left.html"]'
        ),
        Setting(
            scope=Journal.objects.get(
                plant=Plant.objects.get(name='electrolysis'),
                name='electrolysis_technical_report_12_degree'
            ),
            name='tables_list',
            value='["tables/electrolysis/electrolysis_technical_report_12_degree/right.html", "tables/electrolysis/electrolysis_technical_report_12_degree/left.html"]'
        ),
        Setting(
            scope=Journal.objects.get(
                plant=Plant.objects.get(name='electrolysis'),
                name='electrolysis_repair_report_tables'
            ),
            name='tables_list',
            value='["tables/electrolysis/electrolysis_repair_report_tables/main.html"]'
        ),
        Setting(
            scope=Journal.objects.get(
                plant=Plant.objects.get(name='leaching'),
                name='leaching_repair_equipment'
            ),
            name='tables_list',
            value='["tables/leaching/leaching_repair_equipment/repair.html"]'
        ),
        Setting(
            scope=Journal.objects.get(
                plant=Plant.objects.get(name='leaching'),
                name='leaching_express_analysis'
            ),
            name='tables_list',
            value='["tables/leaching/leaching_express_analysis/tanks_availability.html", "tables/leaching/leaching_express_analysis/appt_hydrometal.html", "tables/leaching/leaching_express_analysis/reagents.html", "tables/leaching/leaching_express_analysis/neutral.html", "tables/leaching/leaching_express_analysis/zinc_pulp.html", "tables/leaching/leaching_express_analysis/tanks_for_finished_products.html", "tables/leaching/leaching_express_analysis/self_protection.html", "tables/leaching/leaching_express_analysis/vsns.html", "tables/leaching/leaching_express_analysis/schieht.html", "tables/leaching/leaching_express_analysis/thickeners.html", "tables/leaching/leaching_express_analysis/sample.html", "tables/leaching/leaching_express_analysis/neutral_thickeners.html", "tables/leaching/leaching_express_analysis/cinder.html", "tables/leaching/leaching_express_analysis/loads.html", "tables/leaching/leaching_express_analysis/shift_info.html", "tables/leaching/leaching_express_analysis/agitators.html"]'
        ),
    ])
