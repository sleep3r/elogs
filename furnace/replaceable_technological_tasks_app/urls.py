
from furnace.replaceable_technological_tasks_app import views
from django.conf.urls import url, include


urlpatterns = [
    url('technologicaltasks/$', views.index),
    url('^$', views.index)
]