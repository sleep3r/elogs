from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from e_logs.common.data_visualization_app.views import GraphView, GraphsListView, AddGraphView

urlpatterns = [
    url('get-graphs-list', GraphsListView.as_view()),
    url('get-graph', csrf_exempt(GraphView.as_view())),
    url('add-graph', csrf_exempt(AddGraphView.as_view())),
]
