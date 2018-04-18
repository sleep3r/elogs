from django.conf.urls import url, include

from leaching.express_anal_app import views
from leaching.express_anal_app.components import agitators, cinder, reagents, ready_tanks, neutural_solution, security, \
    empty_tanks, densers_neutural, shift_info, schiehta, electrolysis, sample2, veu, shifts, express_analysis, hydrometal, \
    pulps


urlpatterns = [
    url('journal$', views.leaching_jurnal),
    url('journal/timeing$', express_analysis.express),

    url('all/edit$', views.leaching_all_edit),
    url('edit/wizard$', views.leaching_edit_wizard),
    url('page/wizard$', views.leaching_wizard),

    url('notifications/read$', views.notifications_read),

    url('api/express/analysis$', views.leaching_api_express_analysis),
    url('save/express/analysis/json$', views.leaching_save_express_analysis_json),
    url('save/self/security/json$', views.leaching_save_self_security_json),

    url('save/express/analysis$', views.leaching_save_express_analysis),
    url('save/self/security$', views.leaching_save_self_security),

    url('api/hydrometal$', hydrometal.leaching_api_hydrometal),
    url('save/hydrometal$', views.leaching_save_hydrometal),
    url('save/hydrometal/json$', hydrometal.leaching_save_hydrometal_json),
    url('update/hydrometal$', hydrometal.leaching_update_hydrometal),
    url('api/hydrometal/remove$', hydrometal.leaching_save_hydrometal_remove),

    url('save/pulps$', pulps.leaching_save_pulps),
    url('api/pulps$', pulps.get_table),
    url('pulps/add', pulps.add_record),
    url('pulps/update$', pulps.leaching_update_pulps),
    url('api/pulps/remove$', pulps.remove_record),

    url('save/sample2$', views.leaching_save_sample2),
    url('save/veu', views.leaching_save_vue),

    url('save/schiehta$', views.leaching_save_schiehta),
    url('save/electrolysis$', views.leaching_save_electrolysis),
    url('save/tanks$', views.leaching_save_tanks),
    url('save/densers/neutural$', views.leaching_save_neutural_densers),

    url('api/densers$', views.leaching_api_densers),
    url('save/densers$', views.leaching_save_densers),
    url('save/densers/json$', views.leaching_save_densers_json),

    url('api/agitators$', agitators.leaching_api_agitators),
    url('save/agitators$', agitators.leaching_save_agitators),
    url('agitators/save$', agitators.save_record),
    url('agitators/add$', agitators.add_record),

    url('save/cinder$', views.leaching_save_cinder),
    url('cinder$', cinder.leaching_cinder),
    url('cinder/add$', cinder.add_record),
    url('cinder/save$', cinder.save_record),

    url('reagents$', reagents.get_table),
    url('reagents/save$', reagents.save_record),
    url('reagents/add$', reagents.add_record),

    url('ready/tanks$', ready_tanks.get_table),
    url('ready/tanks/save$', ready_tanks.save_record),
    url('ready/tanks/add$', ready_tanks.add_record),

    url('empty/tanks$', empty_tanks.get_table),
    url('empty/tanks/save$', empty_tanks.save_record),
    url('empty/tanks/add$', empty_tanks.add_record),

    url('neutural/solution$', neutural_solution.get_table),
    url('neutural/solution/save$', neutural_solution.save_record),
    url('neutural/solution/add$', neutural_solution.add_record),
    url('save/neutural/solution', views.leaching_save_neutural_solution),

    url('self/security$', security.get_table),
    url('self/security/save$', security.save_record),
    url('self/security/add$', security.add_record),

    url('densers/neutural$', densers_neutural.get_table),
    url('densers/neutural/save$', densers_neutural.save_record),
    url('densers/neutural/add$', densers_neutural.add_record),

    url('shift/info$', shift_info.get_table),
    url('shift/info/save$', shift_info.save_record),
    url('shift/info/add$', shift_info.add_record),

    url('schiehta$', schiehta.get_table),
    url('schiehta/save$', schiehta.save_record),
    url('schiehta/add$', schiehta.add_record),

    url('electrolysis$', electrolysis.get_table),
    url('electrolysis/save$', electrolysis.save_record),
    url('electrolysis/add$', electrolysis.add_record),

    url('sample2$', sample2.get_table),
    url('sample2/save$', sample2.save_record),
    url('sample2/add$', sample2.add_record),

    url('veu$',  veu.get_table),
    url('veu/save$',  veu.save_record),
    url('veu/add$',  veu.add_record),

    url('save/shift/info$', views.leaching_save_shift_info),
    url('save/empty/tanks$', views.leaching_save_empty_tanks),

    url('json/test$', views.json_test),
    url('json/densers$', views.json_densers),

    url('shift/make$', views.leaching_make_shift),
    url('shift/accessible$', shifts.accessible_shifts),
]