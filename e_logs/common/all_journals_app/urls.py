from django.conf.urls import url, include
from django.urls import path

from e_logs.common.all_journals_app import views


urlpatterns = [
    url('change_table$', views.change_table),
    url('fields_info/$', views.get_fields_descriptions),
    url('add_responsible$', views.add_responsible),
    url('send-message-to-devs$', views.send_message_to_devs),
]
