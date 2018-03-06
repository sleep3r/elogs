from django.conf.urls import url, include

from express_anal_app import views

urlpatterns = [
    url('^$', views.index),
    url('jea/edit$', views.leaching_jea_edit),
    url('jea', views.leaching_jea),
    url('ju', views.leaching_ju),
    url('jrk', views.leaching_jrk),
    url('main', views.electrolysis),
    url('edit$', views.electrolysisEdit)
]