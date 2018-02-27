from django.conf.urls import url, include

from express_anal_app import views

urlpatterns = [
    url('^$', views.index),
]