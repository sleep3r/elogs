from e_logs.electrolysis.masters_raports_app import views
from django.conf.urls import url

urlpatterns = [
    url('^$', views.index)
]
