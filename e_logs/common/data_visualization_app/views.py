from django.shortcuts import render
from cacheops import cached_view_as
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.generic.list import ListView
from django.views.decorators.csrf import csrf_exempt
from e_logs.core.utils.webutils import process_json_view
from e_logs.common.messages_app.models import Message
from e_logs.core.models import Setting
from e_logs.common.login_app.models import Employee
from e_logs.common.all_journals_app.models import Cell, Shift, Journal, Table, Field
from e_logs.core.utils.deep_dict import DeepDict
from e_logs.core.utils.errors import AccessError
from e_logs.core.utils.webutils import model_to_dict, logged, process_json_view
from json_tricks import dumps, loads
import datetime
import json
import plotly.graph_objs as go


# Create your views here.

def get_data(field, employee=None, period=7):
    cells = Cell.objects.filter(field=field)
    shifts = []
    end = datetime.datetime.date(datetime.datetime.now())
    start = end - datetime.timedelta(days=period)

    for cell in cells:
        group = cell.group
        shift = Shift.objects.get(id=group.id)
        shifts.append(shift)

    cells_w_dates = [{"cell": cell, "date": shift.date} for cell, shift in zip(cells, shifts) if shift.date >= start]
    sorted(cells_w_dates, key=lambda x: x["date"])
    values = [int(item["cell"].value) for item in cells_w_dates]
    dates = [item["date"] for item in cells_w_dates]
    return values, dates


def line(x, y):
    trace = go.Scatter(x=x, y=y);
    layout = {"title": 'Average High and Low Temperatures in New York'}
    fig = go.Figure(data=[trace], layout=layout)
    return fig.to_plotly_json()


class GraphsListView(LoginRequiredMixin, View):
    @logged
    def get(self, request):
        employee = Employee.objects.get(user=request.user)
        graphs = Setting.get_value(name="graphs", employee=employee)
        return JsonResponse({"graphs": graphs})


class GraphView(LoginRequiredMixin, View):
    @logged
    def post(self, request):
        field_id = json.loads(request.body)
        field = Field(id=field_id)
        y, x = get_data(field)
        print(x, y)
        graph = line(x, y)
        print(dumps(graph, primitives=True))
        return HttpResponse(dumps(graph, primitives=True),
            content_type='application/json; charset=utf8')


class AddGraphView(LoginRequiredMixin, View):
    @logged
    def post(self, request):
        employee = Employee.objects.get(user=request.user)
        print(request.body)
        cell_info = json.loads(request.body)
        journal_name = cell_info["journal_name"]
        table_name = cell_info["table_name"]
        field_name = cell_info["field_name"]
        journal = Journal.objects.get(name=journal_name)
        table = Table.objects.get(name=table_name, journal_id=journal.id)
        field = Field.objects.get(name=field_name, table_id=table.id)

        graphs = Setting.get_value(name="graphs", employee=employee)
        if graphs is None:
            graphs = []
        graphs.append(field.id)
        Setting.set_value(name="graphs", employee=employee, value=graphs)

        return JsonResponse({"result": 1})
