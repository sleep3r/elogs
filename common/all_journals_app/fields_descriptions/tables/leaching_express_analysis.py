from common.all_journals_app.fields_descriptions.fields_classes import *
from utils.deep_dict import deep_dict


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

#------------------

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

#----------

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



