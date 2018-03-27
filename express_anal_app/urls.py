from django.conf.urls import url, include

from express_anal_app import views

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
    url('leaching/api/hydrometal/remove$', views.leaching_save_hydrometal_remove),


    url('save/sample2$', views.leaching_save_sample2),
    url('save/veu', views.leaching_save_vue),
    url('save/cinder$', views.leaching_save_cinder),
    url('save/schiehta$', views.leaching_save_schiehta),
    url('save/electrolysis$', views.leaching_save_electrolysis),
    url('save/tanks$', views.leaching_save_tanks),
    url('save/densers/neutural$', views.leaching_save_neutural_densers),

    url('leaching/api/densers$', views.leaching_api_densers),
    url('save/densers$', views.leaching_save_densers),
    url('save/densers/json$', views.leaching_save_densers_json),

    url('save/pulps$', views.leaching_save_pulps),

    url('save/agitators$', views.leaching_save_agitators),
    url('save/shift/info$', views.leaching_save_shift_info),
    url('save/empty/tanks$', views.leaching_save_empty_tanks),
    url('save/neutural/solution', views.leaching_save_neutural_solution),



    url('ju', views.leaching_ju),
    url('json/test$', views.json_test),
    url('json/densers$', views.json_densers)
]