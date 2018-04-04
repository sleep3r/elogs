from django.conf.urls import url, include

from leaching.express_anal_app import views
from leaching.express_anal_app.components import agitators, cinder, reagents, ready_tanks


urlpatterns = [
    url('^$', views.index),
    # url('jea/edit$', views.leaching_jea_edit),
    url('all/edit$', views.leaching_all_edit),
    url('page/wizard$', views.leaching_wizard),


    url('leaching/api/express/analysis$', views.leaching_api_express_analysis),
    url('save/express/analysis/json$', views.leaching_save_express_analysis_json),
    url('save/self/security/json$', views.leaching_save_self_security_json),

    url('save/express/analysis$', views.leaching_save_express_analysis),
    url('save/self/security$', views.leaching_save_self_security),


    url('leaching/api/hydrometal$', views.leaching_api_hydrometal),
    url('save/hydrometal$', views.leaching_save_hydrometal),
    url('save/hydrometal/json$', views.leaching_save_hydrometal_json),
    url('leaching/update/hydrometal$', views.leaching_update_hydrometal),
    url('leaching/api/hydrometal/remove$', views.leaching_save_hydrometal_remove),

    url('save/pulps$', views.leaching_save_pulps),
    url('leaching/api/pulps$', views.leaching_api_pulps),
    url('leaching/update/pulps$', views.leaching_update_pulps),
    url('leaching/api/pulps/remove$', views.leaching_pulps_remove),

    url('save/sample2$', views.leaching_save_sample2),
    url('save/veu', views.leaching_save_vue),

    url('save/schiehta$', views.leaching_save_schiehta),
    url('save/electrolysis$', views.leaching_save_electrolysis),
    url('save/tanks$', views.leaching_save_tanks),
    url('save/densers/neutural$', views.leaching_save_neutural_densers),

    url('leaching/api/densers$', views.leaching_api_densers),
    url('save/densers$', views.leaching_save_densers),
    url('save/densers/json$', views.leaching_save_densers_json),

    url('leaching/api/agitators$', agitators.leaching_api_agitators),
    url('save/agitators$', agitators.leaching_save_agitators),
    url('leaching/agitators/update$', agitators.update_agitators),
    url('leaching/agitators/add$', agitators.add_record),

    url('save/cinder$', views.leaching_save_cinder),
    url('leaching/cinder$', cinder.leaching_cinder),
    url('leaching/cinder/add$', cinder.add_record),
    url('leaching/cinder/save$', cinder.save_record),

    url('leaching/reagents$', reagents.get_table),
    url('leaching/reagents/save$', reagents.save_record),
    url('leaching/reagents/add$', reagents.add_record),

    url('leaching/ready/tanks$', ready_tanks.get_table),
    url('leaching/ready/tanks/save$', ready_tanks.save_record),
    url('leaching/ready/tanks/add$', ready_tanks.add_record),

    url('save/shift/info$', views.leaching_save_shift_info),
    url('save/empty/tanks$', views.leaching_save_empty_tanks),
    url('save/neutural/solution', views.leaching_save_neutural_solution),



    url('leaching/journal$', views.leaching_jurnal),
    url('json/test$', views.json_test),
    url('json/densers$', views.json_densers),

    url('leaching/shift/make$', views.leaching_make_shift)
]