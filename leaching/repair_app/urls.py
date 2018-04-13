from django.conf.urls import url, include
from leaching.repair_app import views


urlpatterns = [
    url('edit$', views.edit),
    url('allitems$', views.get_items),
    url('add', views.add_record),
    url('save', views.save_record),
    url('remove', views.remove_record),
    url('$', views.index),
]