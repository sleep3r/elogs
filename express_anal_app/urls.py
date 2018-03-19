from django.conf.urls import url, include

from express_anal_app import views

urlpatterns = [
    url('^$', views.index),
    url('jea/edit$', views.leaching_jea_edit),
    url('all/edit$', views.leaching_all_edit),
    url('save/tanks$', views.leaching_save_tanks),
    url('save/densers/neutural$', views.leaching_save_neutural_densers),
    url('save/express/analysis$', views.leaching_save_express_analysis),
    url('save/densers$', views.leaching_save_densers),
    url('save/pulps$', views.leaching_save_pulps),
    url('save/hydrometal$', views.leaching_save_hydrometal),
    url('save/agitators$', views.leaching_save_agitators),
    url('jea', views.leaching_jea),
    url('ju', views.leaching_ju),
    url('jrk', views.leaching_jrk),
    url('main', views.electrolysis),
    url('edit$', views.electrolysisEdit)
]