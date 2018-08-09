from django.conf.urls import url

from e_logs.furnace.fractional_app import views

urlpatterns = [
    url('measurements/get$', views.granularity_object),
    url('measurements/post', views.add_measurement),
    url('granularity_graphs/get$', views.granularity_graphs),
    url('^$', views.Index.as_view())
]
