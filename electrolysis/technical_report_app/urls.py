from electrolysis.technical_report_app import views
from django.conf.urls import url, include
from django.urls import path

urlpatterns = [
    # url('technical', views.granularity_object),
    url('^$', views.index)
]
