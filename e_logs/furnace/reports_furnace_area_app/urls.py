from e_logs.furnace.reports_furnace_area_app import views
from django.conf.urls import url

urlpatterns = [
    url('^$', views.index)
]
