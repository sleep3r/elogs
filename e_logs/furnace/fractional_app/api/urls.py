from django.conf.urls import url, include
from django.urls import path, re_path

from .views import MeasurementRUD, MeasurementAPI, MeasurementGraphs


urlpatterns = [
    path('', MeasurementAPI.as_view()),
    re_path(r'(?P<id>\d+)$', MeasurementRUD.as_view()),
    path('graphs', MeasurementGraphs.as_view()),
]
