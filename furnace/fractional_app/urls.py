from furnace.fractional_app import views

from django.conf.urls import url, include
from django.urls import path

urlpatterns = [
    url('measurements/get$', views.granularity_object),
]