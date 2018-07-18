from e_logs.electrolysis.technical_report_app3 import views
from django.conf.urls import url, include
from django.urls import path

urlpatterns = [
    url('^$', views.index)
]
