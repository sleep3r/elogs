
from furnace.changed_fraction_app import views
from django.conf.urls import url


urlpatterns = [
    url('^$', views.index)
]