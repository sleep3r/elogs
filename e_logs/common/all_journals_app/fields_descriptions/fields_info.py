import ast

from e_logs.common.all_journals_app.fields_descriptions.tables.change_fraction import change_fraction_table_desc
from e_logs.common.all_journals_app.fields_descriptions.tables.conc_raports_tables import *
from e_logs.common.all_journals_app.fields_descriptions.tables.electrolysis_masters_reports import *
from e_logs.common.all_journals_app.fields_descriptions.tables.furnace_repair import *
from e_logs.common.all_journals_app.fields_descriptions.tables.furnace_stove_area import *
from e_logs.common.all_journals_app.fields_descriptions.tables.input_output_report import *
from e_logs.common.all_journals_app.fields_descriptions.tables.leaching_express_analysis import *
from e_logs.common.all_journals_app.fields_descriptions.tables.leaching_repair_equipment import leaching_repair_table_desc
from e_logs.common.all_journals_app.fields_descriptions.tables.metals_compute import *
from e_logs.common.all_journals_app.fields_descriptions.tables.electrolysis_technical_report_4_degree_tables import *
from e_logs.common.all_journals_app.fields_descriptions.tables.technological_tasks import *
import e_logs.common.all_journals_app.fields_descriptions.tables.electrolysis_technical_report_3_degree_tables as t3
import e_logs.common.all_journals_app.fields_descriptions.tables.electrolysis_technical_report_12_degree_tables as t12
from e_logs.common.all_journals_app.fields_descriptions.tables.electrolysis_repair_report_tables import *
from e_logs.core.models import Setting
from e_logs.common.all_journals_app.models import Field, Table, Journal


from e_logs.core.utils.deep_dict import deep_dict

fields_info_desc = deep_dict()

fields_info_desc.leaching_express_analysis.vsns= vsns_table_desc
fields_info_desc.leaching_express_analysis.thickeners= thickeners_table_desc
fields_info_desc.leaching_express_analysis.zinc_pulp= zinc_pulp_desc
fields_info_desc.leaching_express_analysis.appt_hydrometal= aph_table_desc
fields_info_desc.leaching_express_analysis.agitators= agitator_table_desc
fields_info_desc.leaching_express_analysis.reagents= reagents_table_desc
fields_info_desc.leaching_express_analysis.neutral_thickeners= neutral_thickeners_desc
fields_info_desc.leaching_express_analysis.tanks_availability= tanks_availability_desc
fields_info_desc.leaching_express_analysis.tanks_for_finished_products= tanks_for_finished_products_desc
fields_info_desc.leaching_express_analysis.self_protection= self_protection_desc
fields_info_desc.leaching_express_analysis.cinder= cinder_table_desc
fields_info_desc.leaching_express_analysis.sample= sample_table_desc
fields_info_desc.leaching_express_analysis.loads= loads_table_desc
fields_info_desc.leaching_express_analysis.neutral= neutral_table_desc
fields_info_desc.leaching_express_analysis.shift_info= shift_info_table_desc

fields_info_desc.leaching_repair_equipment.repair= leaching_repair_table_desc

fields_info_desc.concentrate_report.big= big_table_desc
fields_info_desc.concentrate_report.small= small_table_desc
fields_info_desc.concentrate_report.upper= upper_table_desc
fields_info_desc.concentrate_report.lower= lower_table_desc

fields_info_desc.report_income_outcome_schieht.main= main_table_desc
fields_info_desc.report_income_outcome_schieht.supply_of_zinc_concentrates = supply_zinc_desc
fields_info_desc.report_income_outcome_schieht.year_plan_schieht = year_plan_schieht_desc
fields_info_desc.report_income_outcome_schieht.summary= summary_table_desc

fields_info_desc.metals_compute.main= metals_main_desc
fields_info_desc.metals_compute.sns= sns_table_desc
fields_info_desc.metals_compute.sgok= sgok_table_desc
fields_info_desc.metals_compute.gof= gof_table_desc
fields_info_desc.metals_compute.avg_month= avg_month_table_desc
fields_info_desc.metals_compute.cinder_conc= cinder_conc_table_desc
fields_info_desc.metals_compute.concentrat= concentrat_table_desc
fields_info_desc.metals_compute.contain_zn= contain_zn_table_desc


fields_info_desc.technological_tasks.main= technologial_tasks_main_desc
fields_info_desc.furnace_repair.repair= repair_table_desc
fields_info_desc.furnace_changed_fraction.main= change_fraction_table_desc

fields_info_desc.electrolysis_technical_report_4_degree.left= left_table_desc
fields_info_desc.electrolysis_technical_report_4_degree.right= right_table_desc
fields_info_desc.electrolysis_technical_report_3_degree.left= t3.left_table_desc
fields_info_desc.electrolysis_technical_report_3_degree.right= t3.right_table_desc
fields_info_desc.electrolysis_technical_report_12_degree.left= t12.left_table_desc
fields_info_desc.electrolysis_technical_report_12_degree.right= t12.right_table_desc
fields_info_desc.electrolysis_repair_report_tables.main= repair_main_table_desc

fields_info_desc.masters_report.seria1= seria1_table_desc
fields_info_desc.masters_report.seria3= seria3_table_desc
fields_info_desc.masters_report.seria4= seria4_table_desc
fields_info_desc.masters_report.params= params_table_desc
fields_info_desc.masters_report.melt_area1= melt_area1_table_desc
fields_info_desc.masters_report.melt_area2= melt_area2_table_desc
fields_info_desc.masters_report.zinc= zinc_table_desc
fields_info_desc.masters_report.last= last_table_desc


fields_info_desc.reports_furnace_area.main= fa_main_table_desc
fields_info_desc.reports_furnace_area.udel= udel_table_desc
fields_info_desc.reports_furnace_area.area_class_cinder = page1_table3_desc
fields_info_desc.reports_furnace_area.electrofilter = electro_filters_desc
fields_info_desc.reports_furnace_area.warehouse_concentrates = wh_concentrates_desc
fields_info_desc.reports_furnace_area.airmachines = air_machines_desc
fields_info_desc.reports_furnace_area.fences= page1_fences_desc

fields_info_desc.reports_furnace_area.concentration_by_time= page2_table1_desc
fields_info_desc.reports_furnace_area.places_of_sampling= page2_table2_desc
fields_info_desc.reports_furnace_area.corrective_actions= page2_table3_desc
fields_info_desc.reports_furnace_area.self_protection= page2_table4_desc
fields_info_desc.reports_furnace_area.worth= page2_table5_desc


bf = deep_dict()
bf.column1 = numeric_default
bf.column2 = numeric_default
bf.column3 = numeric_default


# for journal in Journal.objects.all():
#     for table in Table.objects.filter(journal=journal):
#         for field in Field.objects.filter(table=table):
#             settings = Setting.objects.filter(name='field_descriptions', field=field)
#             for setting in settings:
#                 description = ast.literal_eval(setting.value)
#                 fields_info_desc[journal.name][table.name][field.name] = description
