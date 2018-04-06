from django.conf.urls import url, include

from login_app import views
urlpatterns = [
    url(r'logout$', views.logout_view),
    url(r'login$', views.login_auth),
    url(r'login_page$', views.login_page),
]

