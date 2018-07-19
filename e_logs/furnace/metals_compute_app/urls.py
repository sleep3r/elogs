
from e_logs.furnace.metals_compute_app import views
from django.conf.urls import url, include


urlpatterns = [
    url('metals$', views.index),
    url('^$', views.index)
]
