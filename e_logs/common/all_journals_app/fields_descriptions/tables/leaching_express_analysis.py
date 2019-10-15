from e_logs.common.all_journals_app.fields_descriptions.fields_classes import *
from e_logs.core.utils.deep_dict import DeepDict


shift_info = DeepDict()
shift_info.this_master = text_default
shift_info.next_master = text_default
shift_info.out_sol_t = ton_default
shift_info.out_sol_c = ton_default
shift_info.out_pulp_cvck = ton_default
shift_info.out_cu_kek = m3_default
shift_info.out_cd_sponge = ton_default
shift_info.out_neutr = m3_default
shift_info.out_Cd = m3_default
shift_info.neutral_hmc = m3_default
shift_info.out_cu_pulp = m3_default
shift_info.in_filtrate_ls = m3_default
shift_info.in_fe = m3_default
shift_info.in_filtrate_dens = numeric_default
shift_info.in_fe_hi = m3_default
shift_info.in_poor_cd = m3_default


shift_info_table_desc = shift_info.clear_empty().get_dict()


vsns = DeepDict()
vsns.time = time_default
vsns.vsns_cobalt = mgl_default
vsns.vsns_Sb = mgl_default
vsns.vsns_Cu = mgl_default
vsns.vsns_Cd = mgl_default
vsns.vsns_solid_after = gl_default
vsns.vsns_pH = ph_default
vsns.vsns_Fe = mgl_default
vsns.vsns_As = mgl_default
vsns.vsns_solid = gl_default
vsns.vsns_density = gsm3_default
vsns.larox_Co = mgl_default
vsns.larox_Sb = mgl_default
vsns.larox_Cd = mgl_default
vsns.larox_solid = gl_default
vsns.larox_pH = ph_default
vsns.liq_Cd = mgl_default
vsns.liq_Co = mgl_default
vsns.liq_Sb = mgl_default
vsns.liq_Cu = mgl_default
vsns.liq_Fe = mgl_default
vsns.liq_current_out = percent_default
vsns.liq_density = gsm3_default
vsns.mng_norm = mgl_default
vsns.mng_fact = mgl_default
vsns.mng_discrepancy = mgl_default
vsns.master = text_default
vsns_table_desc = vsns.clear_empty().get_dict()


thickeners = DeepDict()
thickeners.time = time_default
thickeners.vs10_pH = ph_default
thickeners.vs10_Cu = mgl_default
thickeners.vs10_Fe = mgl_default
thickeners.vs10_liquid_solid = numeric_default
thickeners.ns10_pH = ph_default
thickeners.ns10_liquid_solid = numeric_default

thickeners.vs11_pH = ph_default
thickeners.vs11_Cu = mgl_default
thickeners.vs11_Fe = mgl_default
thickeners.vs11_liquid_solid = numeric_default
thickeners.ns11_pH = ph_default
thickeners.ns11_liquid_solid = numeric_default
thickeners.vs12_pH = ph_default
thickeners.vs12_Cu = mgl_default
thickeners.vs12_Fe = mgl_default
thickeners.vs12_liquid_solid = numeric_default
thickeners.ns12_pH = ph_default
thickeners.ns12_liquid_solid = numeric_default
thickeners_table_desc = thickeners.clear_empty().get_dict()


zinc_pulp = DeepDict()
zinc_pulp.zn_pulp_liquid_solid = numeric_default
zinc_pulp.zn_pulp_pH = ph_default
zinc_pulp.zn_pulp_temperature = temperature_default
zinc_pulp.cu_pulp_liquid_solid = numeric_default
zinc_pulp.cu_pulp_before = gl_default
zinc_pulp.cu_pulp_after = gl_default
zinc_pulp.cu_pulp_tv = gl_default
zinc_pulp.iron_solution_h2so4 = mgl_default
zinc_pulp.iron_solution_tv = mgl_default
zinc_pulp.iron_solution_Sb = mgl_default
zinc_pulp.iron_solution_Cu = mgl_default
zinc_pulp.iron_solution_Fe = mgl_default
zinc_pulp.iron_solution_specific_weight = mgl_default
zinc_pulp.iron_solution_As = mgl_default
zinc_pulp.iron_solution_Cl = mgl_default
zinc_pulp.concentrate_Shlippe = gl_default
zinc_pulp.active_PAV = mhour_default
zinc_pulp.high_Fe = numeric_default
zinc_pulp_desc = zinc_pulp.clear_empty().get_dict()

aph = DeepDict()
aph.mann1_pH = ph_default
aph.mann1_acid = gl_default
aph.mann1_Fe2 = mgl_default
aph.mann1_Fe = mgl_default
aph.mann4_pH = ph_default
aph.mann4_Cu = mgl_default
aph.mann4_Fe = mgl_default
aph.mann4_Sb = mgl_default
aph.mann4_ots = mm_default
aph.sit_cinder1 = mm_default
aph.sit_cinder2 = mm_default
aph.sit_cinder3 = mm_default
aph.sit_cinder4 = mm_default
aph.sit_cinder5 = mm_default
aph.sit_cinder6 = mm_default
aph.sit_cinder_avg = mm_default
aph.fe_avg = mm_default
aph.fe_shave = mgl_default
aph_table_desc = aph.clear_empty().get_dict()


agt = DeepDict()
agt.a1314_Cd_before1 = mgl_default
agt.a1314_Cu_before1 = mgl_default
agt.a1314_Co_before1 = mgl_default
agt.a15_pH_before1 = mgl_default
agt.a15_Cu_before1 = mgl_default
agt.a17_pH_before1 = mgl_default
agt.a17_Cu_before1 = mgl_default
agt.a19_H2SO4_before1 = mgl_default
agt.a19_Cu_before1 = mgl_default

agt.a1314_Cd_before2 = mgl_default
agt.a1314_Cu_before2 = mgl_default
agt.a1314_Co_before2 = mgl_default
agt.a15_pH_before2 = mgl_default
agt.a15_Cu_before2 = mgl_default
agt.a17_pH_before2 = mgl_default
agt.a17_Cu_before2 = mgl_default
agt.a19_H2SO4_before2 = mgl_default
agt.a19_Cu_before2 = mgl_default

agt.a1314_Cd_before3 = mgl_default
agt.a1314_Cu_before3 = mgl_default
agt.a1314_Co_before3 = mgl_default
agt.a15_pH_before3 = mgl_default
agt.a15_Cu_before3 = mgl_default
agt.a17_pH_before3 = mgl_default
agt.a17_Cu_before3 = mgl_default
agt.a19_H2SO4_before3 = mgl_default
agt.a19_Cu_before3 = mgl_default

agt.a1314_Cd_after1 = mgl_default
agt.a1314_Cu_after1 = mgl_default
agt.a1314_Co_after1 = mgl_default
agt.a15_pH_after1 = mgl_default
agt.a15_Cu_after1 = mgl_default
agt.a17_pH_after1 = mgl_default
agt.a17_Cu_after1 = mgl_default
agt.a19_H2SO4_after1 = mgl_default
agt.a19_Cu_after1 = mgl_default

agt.a1314_Cd_after2 = mgl_default
agt.a1314_Cu_after2 = mgl_default
agt.a1314_Co_after2 = mgl_default
agt.a15_pH_after2 = mgl_default
agt.a15_Cu_after2 = mgl_default
agt.a17_pH_after2 = mgl_default
agt.a17_Cu_after2 = mgl_default
agt.a19_H2SO4_after2 = mgl_default
agt.a19_Cu_after2 = mgl_default

agt.a1314_Cd_after3 = mgl_default
agt.a1314_Cu_after3 = mgl_default
agt.a1314_Co_after3 = mgl_default
agt.a15_pH_after3 = mgl_default
agt.a15_Cu_after3 = mgl_default
agt.a17_pH_after3 = mgl_default
agt.a17_Cu_after3 = mgl_default
agt.a19_H2SO4_after3 = mgl_default
agt.a19_Cu_after3 = mgl_default
agt.journal_comment = text_default
agitator_table_desc = agt.clear_empty().get_dict()


rt = DeepDict()
rt.delivery_salt = kg_default
rt.delivery_Zn_dust = numeric_default
rt.delivery_Mn_ore = tn_default
rt.delivery_Magnaflok = kg_default
rt.delivery_Fe_shave = kg_default
rt.income_salt = kg_default
rt.income_Zn_dust = numeric_default
rt.income_Mn_ore = tn_default
rt.income_Magnaflok = kg_default
rt.income_Fe_shave = kg_default
rt.outcome_salt = kg_default
rt.outcome_Zn_1st = ton_default
rt.outcome_Zn_2st = ton_default
rt.outcome_Zn_3st = ton_default
rt.outcome_Zn_Cd = tn_default
rt.outcome_Mn_ore = tn_default
rt.outcome_Magnaflok = kg_default
rt.outcome_Fe_shave = kg_default
rt.passed_salt = kg_default
rt.passed_Zn_dust = numeric_default
rt.passed_Mn_ore = tn_default
rt.passed_Magnaflok = kg_default
rt.passed_Fe_shave = kg_default
rt.state_fances = text_default
reagents_table_desc = rt.clear_empty().get_dict()


tanks_availability = DeepDict()
db_names = [
'prev_measurements_waste_tank_1-2seria', 'current_measurements_waste_tank_1-2seria', 'divergence_waste_tank_1-2seria',
'prev_measurements_manns_1-9', 'current_measurements_manns_1-9', 'divergence_manns_1-9',
'prev_measurements_manns_VTV_10-12', 'current_measurements_manns_VTV_10-12', 'divergence_manns_VTV_10-12',
'prev_measurements_thickener-9', 'current_measurements_thickener-9', 'divergence_thickener-9',
'prev_measurements_agitator-22', 'current_measurements_agitator-22', 'divergence_agitator-22',
'prev_measurements_neutral_tank', 'current_measurements_neutral_tank', 'divergence_neutral_tank',
'prev_measurements_waste_mann-2', 'current_measurements_waste_mann-2', 'divergence_waste_mann-2',
'prev_measurements_waste_mann-3', 'current_measurements_waste_mann-3', 'divergence_waste_mann-3',
'prev_measurements_waste_mann-9', 'current_measurements_waste_mann-9', 'divergence_waste_mann-9',
'prev_measurements_-', 'current_measurements_-', 'divergence_-',
'prev_measurements_removable_balance', 'current_measurements_removable_balance', 'divergence_removable_balance',
'prev_measurements_daily_balance', 'current_measurements_daily_balance', 'divergence_daily_balance']
for name in db_names:
    tanks_availability[name] = numeric_default
tanks_availability_desc = tanks_availability.clear_empty().get_dict()


neutral_thickeners = DeepDict()
sediment = ["sediment"+str(i+1) for i in range(8)] + ["sediment13"]
liquid_solid = ["liquid_solid"+str(i+1) for i in range(8)] + ["liquid_solid13"]
for name in sediment:
    neutral_thickeners[name] = sm_default
for name in liquid_solid:
    neutral_thickeners[name] = numeric_default
neutral_thickeners_desc = neutral_thickeners.clear_empty().get_dict()


self_protection = DeepDict()
self_protection.visiting_time = time_default
self_protection.visiting = text_default
self_protection.notation = text_default
self_protection_desc = self_protection.clear_empty().get_dict()
cn = DeepDict()
cn.shift_total = numeric_default
cn.day_total = numeric_default
cn.in_process = numeric_default
cinder_table_desc = cn.clear_empty().get_dict()


schieht = DeepDict()
schieht.value = numeric_default
schieht.name = text_default
schieht_table_desc = schieht.clear_empty().get_dict()


tanks_for_finished_products = DeepDict()
num_names = ["VT_tank", "specific_weight_tank", "norm_tank", "fact_tank"]
mgl_names = ["Cd_tank", "Cu_tank", "Co_tank", "Sb_tank", "Fe_tank"]
text_names = ["correction_tank", "master_tank"]

for tank in '345':
    for name in mgl_names:
        tanks_for_finished_products[name+tank] = mgl_default
    for name in text_names:
        tanks_for_finished_products[name+tank] = text_default
    for name in num_names:
        tanks_for_finished_products[name+tank] = numeric_default

tanks_for_finished_products_desc = tanks_for_finished_products.clear_empty().get_dict()


loads = DeepDict()
loads.time7 = amper_default
loads.time12 = amper_default
loads.counter = amper_default
loads.bunker_cvco = amper_default
loads.silos = amper_default
loads.bunkers_oc = amper_default

loads.description = text_default
loads_table_desc = loads.clear_empty().get_dict()

sample = DeepDict()
sample.time = time_default
sample.Cd = numeric_default
sample.Cu = numeric_default
sample.VIU1 = numeric_default
sample.VIU2 = numeric_default
sample.VIU3 = numeric_default
sample_table_desc = sample.clear_empty().get_dict()

neutral = DeepDict()
neutral.neutral_solution = numeric_default
neutral.leach1 = numeric_default
neutral.leach2 = numeric_default
neutral.bak_3 = numeric_default
neutral.bak_4 = numeric_default
neutral.summary = numeric_default
neutral.bak_seria3 = numeric_default
neutral.bak_5 = numeric_default
neutral.bak_6 = numeric_default
neutral_table_desc = neutral.clear_empty().get_dict()
