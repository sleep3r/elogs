from e_logs.leaching.express_analysis_app import views
from django.conf.urls import url

urlpatterns = [
    url('^$', views.index)
]
