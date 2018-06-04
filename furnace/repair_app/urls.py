
from furnace.repair_app import views
from django.conf.urls import url


urlpatterns = [
    url('^$', views.index)
]