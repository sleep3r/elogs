from django.urls import path
from django.conf.urls import url

from e_logs.common.all_journals_app import views

urlpatterns = [
    url(r'save_cell/$', views.save_cell),
    url(r'journal_upload/$', views.ConstructorView.as_view()),
]
