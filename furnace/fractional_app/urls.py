from django.conf.urls import url, include

from furnace.fractional_app import views


urlpatterns = [
    url('^$', views.index)
]