from common.all_journals_app.fields_descriptions.tables.conc_raports_tables import *
from common.all_journals_app.fields_descriptions.tables.input_output_report import *
from common.all_journals_app.fields_descriptions.tables.metals_compute import *


from utils.deep_dict import deep_dict

fields_info_desc = deep_dict()

fields_info_desc.concentrate_report_journal.big_table = big_table_desc
fields_info_desc.concentrate_report_journal.small_table = small_table_desc
fields_info_desc.concentrate_report_journal.upper_fields = upper_table_desc
fields_info_desc.concentrate_report_journal.lower_fields = lower_table_desc

fields_info_desc.report_income_outcome_schieht.main_table = main_table_desc
fields_info_desc.report_income_outcome_schieht.supply_zinc_table = supply_zinc_desc
fields_info_desc.report_income_outcome_schieht.year_plan_schieht = year_plan_schieht_desc
fields_info_desc.report_income_outcome_schieht.summary_table = summary_table_desc

fields_info_desc.metals_compute.metals_compute_table = metals_main_desc
fields_info_desc.metals_compute.sns_table = sns_table_desc
fields_info_desc.metals_compute.sgok_table = sgok_table_desc
fields_info_desc.metals_compute.gof_table = gof_table_desc

# fields_info_desc = fields_info_desc.get_dict()
