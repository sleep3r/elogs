from django.urls import path
from django.conf.urls import url

from e_logs.common.all_journals_app import views

urlpatterns = [
    url(r'change_table$', views.change_table),
    url(r'save_cell/$', views.save_cell),
    url(r'save_table_comment/$', views.save_table_comment),
]
