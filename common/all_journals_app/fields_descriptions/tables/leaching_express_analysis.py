from common.all_journals_app.fields_descriptions.fields_classes import *
from utils.deep_dict import deep_dict


shift_info = deep_dict()
shift_info.this_master = text_default
shift_info.next_master = text_default
shift_info.out_sol_t = text_default
shift_info.out_sol_c = text_default
shift_info.out_pulp_cvck = text_default
shift_info.out_cu_kek = text_default
shift_info.out_cd_sponge = text_default
shift_info.out_neutr = text_default
shift_info.out_Cd = text_default
shift_info.neutral_hmc = text_default
shift_info.out_cu_pulp = text_default
shift_info.in_filtrate_ls = text_default
shift_info.in_filtrate_dens = text_default
shift_info.in_fe_hi = text_default
shift_info.in_poor_cd = text_default


shift_info_table_desc = shift_info.clear_empty().get_dict()


vsns = deep_dict()
vsns.time = time_default
vsns.vsns_cobalt = numeric_default
vsns.vsns_Sb = numeric_default
vsns.vsns_Cu = numeric_default
vsns.vsns_Cd = numeric_default
vsns.vsns_solid_after = numeric_default
vsns.vsns_pH = numeric_default
vsns.vsns_Fe = numeric_default
vsns.vsns_As = numeric_default
vsns.vsns_solid = numeric_default
vsns.vsns_density = numeric_default
vsns.larox_Co = numeric_default
vsns.larox_Sb = numeric_default
vsns.larox_Cd = numeric_default
vsns.larox_solid = numeric_default
vsns.larox_pH = numeric_default
vsns.liq_Cd = numeric_default
vsns.liq_Co = numeric_default
vsns.liq_Sb = numeric_default
vsns.liq_Cu = numeric_default
vsns.liq_Fe = numeric_default
vsns.liq_current_out = numeric_default
vsns.liq_density = numeric_default
vsns.mng_norm = numeric_default
vsns.mng_fact = numeric_default
vsns.mng_correction = numeric_default
vsns.master = text_default
vsns_table_desc = vsns.clear_empty().get_dict()


thickeners = deep_dict()
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


zinc_pulp = deep_dict()
zinc_pulp.zn_pulp_liquid_solid = numeric_default
zinc_pulp.zn_pulp_pH = ph_default
zinc_pulp.zn_pulp_temperature = temperature_default
zinc_pulp.cu_pulp_liquid_solid = numeric_default
zinc_pulp.cu_pulp_before = numeric_default
zinc_pulp.cu_pulp_after = numeric_default
zinc_pulp.cu_pulp_tv = numeric_default
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

aph = deep_dict()
aph.mann1_pH = numeric_default
aph.mann1_acid = numeric_default
aph.mann1_Fe2 = numeric_default
aph.mann1_Fe = numeric_default
aph.mann4_pH = numeric_default
aph.mann4_Cu = numeric_default
aph.mann4_Fe = numeric_default
aph.mann4_Sb = numeric_default
aph.mann4_ots = numeric_default
aph.sit_cinder1 = numeric_default
aph.sit_cinder2 = numeric_default
aph.sit_cinder3 = numeric_default
aph.sit_cinder4 = numeric_default
aph.sit_cinder5 = numeric_default
aph.sit_cinder6 = numeric_default
aph.sit_cinder_avg = numeric_default
aph.fe_avg = numeric_default
aph.fe_shave = numeric_default
aph_table_desc = aph.clear_empty().get_dict()


agt = deep_dict()
agt.a1314_Cd_before1 = numeric_default
agt.a1314_Cu_before1 = numeric_default
agt.a1314_Co_before1 = numeric_default
agt.a15_pH_before1 = numeric_default
agt.a15_Cu_before1 = numeric_default
agt.a17_pH_before1 = numeric_default
agt.a17_Cu_before1 = numeric_default
agt.a19_H2SO4_before1 = numeric_default
agt.a19_Cu_before1 = numeric_default

agt.a1314_Cd_before2 = numeric_default
agt.a1314_Cu_before2 = numeric_default
agt.a1314_Co_before2 = numeric_default
agt.a15_pH_before2 = numeric_default
agt.a15_Cu_before2 = numeric_default
agt.a17_pH_before2 = numeric_default
agt.a17_Cu_before2 = numeric_default
agt.a19_H2SO4_before2 = numeric_default
agt.a19_Cu_before2 = numeric_default

agt.a1314_Cd_before3 = numeric_default
agt.a1314_Cu_before3 = numeric_default
agt.a1314_Co_before3 = numeric_default
agt.a15_pH_before3 = numeric_default
agt.a15_Cu_before3 = numeric_default
agt.a17_pH_before3 = numeric_default
agt.a17_Cu_before3 = numeric_default
agt.a19_H2SO4_before3 = numeric_default
agt.a19_Cu_before3 = numeric_default

agt.a1314_Cd_after1 = numeric_default
agt.a1314_Cu_after1 = numeric_default
agt.a1314_Co_after1 = numeric_default
agt.a15_pH_after1 = numeric_default
agt.a15_Cu_after1 = numeric_default
agt.a17_pH_after1 = numeric_default
agt.a17_Cu_after1 = numeric_default
agt.a19_H2SO4_after1 = numeric_default
agt.a19_Cu_after1 = numeric_default

agt.a1314_Cd_after2 = numeric_default
agt.a1314_Cu_after2 = numeric_default
agt.a1314_Co_after2 = numeric_default
agt.a15_pH_after2 = numeric_default
agt.a15_Cu_after2 = numeric_default
agt.a17_pH_after2 = numeric_default
agt.a17_Cu_after2 = numeric_default
agt.a19_H2SO4_after2 = numeric_default
agt.a19_Cu_after2 = numeric_default

agt.a1314_Cd_after3 = numeric_default
agt.a1314_Cu_after3 = numeric_default
agt.a1314_Co_after3 = numeric_default
agt.a15_pH_after3 = numeric_default
agt.a15_Cu_after3 = numeric_default
agt.a17_pH_after3 = numeric_default
agt.a17_Cu_after3 = numeric_default
agt.a19_H2SO4_after3 = numeric_default
agt.a19_Cu_after3 = numeric_default
agt.journal_comment = text_default
agitator_table_desc = agt.clear_empty().get_dict()


rt = deep_dict()
rt.delivery_salt = numeric_default
rt.delivery_Zn_dust = numeric_default
rt.delivery_Mn_ore = numeric_default
rt.delivery_Magnoflok = numeric_default
rt.delivery_Fe_shave = numeric_default
rt.income_salt = numeric_default
rt.income_Zn_dust = numeric_default
rt.income_Mn_ore = numeric_default
rt.income_Magnaflok = numeric_default
rt.income_Fe_shave = numeric_default
rt.outcome_salt = numeric_default
rt.outcome_Zn_1st = numeric_default
rt.outcome_Zn_2st = numeric_default
rt.outcome_Zn_3st = numeric_default
rt.outcome_Zn_Cd = numeric_default
rt.outcome_Mn_ore = numeric_default
rt.outcome_Magnaflok = numeric_default
rt.outcome_Fe_shave = numeric_default
rt.passed_Zn_dust = numeric_default
rt.passed_Mn_ore = numeric_default
rt.passed_Magnaflok = numeric_default
rt.passed_Fe_shave = numeric_default
rt.state_fances = text_default
reagents_table_desc = rt.clear_empty().get_dict()


tanks_availability = deep_dict()
cols = ['prev_measurements_waste_tank_1-2seria', 'current_measurements_waste_tank_1-2seria', 'divergence_waste_tank_1-2seria',
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
for name in cols:
    tanks_availability[name] = numeric_default
tanks_availability_desc = tanks_availability.clear_empty().get_dict()


neutral_thickeners = deep_dict()
sediment = ["sediment"+str(i+1) for i in range(8)] + ["sediment13"]
liquid_solid = ["liquid_solid"+str(i+1) for i in range(8)] + ["liquid_solid13"]
for name in sediment+liquid_solid:
    neutral_thickeners[name] = numeric_default
neutral_thickeners_desc = neutral_thickeners.clear_empty().get_dict()


self_protection = deep_dict()
self_protection.visiting_time = time_default
self_protection.visiting = text_default
self_protection.notation = text_default
self_protection_desc = self_protection.clear_empty().get_dict()
cn = deep_dict()
cn.shift_total = numeric_default
cn.day_total = numeric_default
cn.in_process = numeric_default
cinder_table_desc = cn.clear_empty().get_dict()


schieht = deep_dict()
schieht.value = numeric_default
schieht.name = text_default
schieht_table_desc = schieht.clear_empty().get_dict()


loads = deep_dict()
loads.time7 = numeric_default
loads.time12 = numeric_default
loads.counter = numeric_default
loads.bunker_cvco = numeric_default
loads.silos = numeric_default
loads.bunkers_oc = numeric_default

loads.description  = text_default
loads_table_desc = loads.clear_empty().get_dict()

sample = deep_dict()
sample.time = time_default
sample.Cd = numeric_default
sample.Cu = numeric_default
sample.VIU1 = numeric_default
sample.VIU2 = numeric_default
sample.VIU3 = numeric_default
sample_table_desc = sample.clear_empty().get_dict()

neutral = deep_dict()
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