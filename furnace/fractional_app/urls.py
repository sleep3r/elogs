from furnace.fractional_app import views
from django.conf.urls import url, include
from django.urls import path

urlpatterns = [
    url('measurements/get$', views.granularity_object),
    url('measurements/post', views.add_measurement),
    url('granularity_gaphs/get$', views.granularity_gaphs),
    url('^$', views.index)
]