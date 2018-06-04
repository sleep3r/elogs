from django.conf.urls import url, include

from main_app import views

urlpatterns = [
    url('^talker/edit$', views.edit_talker),
    url('^list$', views.conference_list),
    url('^tracks$', views.get_conference),
    url('^info$', views.conference_info),
    url('^file/edit$', views.edit_file),
    url('^edit$', views.edit_conference),
    url('^add$', views.add_conference),
    url('^file/drop$', views.drop_file),
    url('^file/cut$', views.cut_file),
    url('^updates$', views.conf_updates),
    url('^file/restore$', views.restore_file),
    url('^tracks/deleted$', views.deleted_files),
]