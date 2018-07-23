from django.conf.urls import url, include

from e_logs.common.login_app import views
urlpatterns = [
    url(r'logout$', views.logout_view),
    url(r'login$', views.login_auth),
    url(r'login_page$', views.login_page),
]
