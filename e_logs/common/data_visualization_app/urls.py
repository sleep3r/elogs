from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from e_logs.common.data_visualization_app.views import *

urlpatterns = [
    url('^$', DashboardView.as_view()),
    url('get-config', DashboardConfigView.as_view()),
    url('update-config', csrf_exempt(DashboardConfigUpdateView.as_view())),
    url('get-graph', csrf_exempt(GraphView.as_view())),
    url('add-graph', csrf_exempt(AddGraphView.as_view())),
    url('delete-graph', csrf_exempt(DeleteGraphView.as_view())),
]
