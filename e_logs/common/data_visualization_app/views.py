from django.shortcuts import render
from cacheops import cached_view_as
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.decorators.csrf import csrf_exempt
from e_logs.core.utils.webutils import process_json_view
from e_logs.common.messages_app.models import Message
from e_logs.common.all_journals_app.services.context_creator import get_menu_data
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

    cells_w_shifts = [{"cell": cell, "shift": shift} for cell, shift in zip(cells, shifts) if shift.date >= start]
    cells_w_shifts = sorted(cells_w_shifts, key=lambda x: x["shift"].start_time)

    values = [int(item["cell"].value) for item in cells_w_shifts]
    shifts = [item["shift"] for item in cells_w_shifts]
    return values, shifts


def timeline(x, y, title):
    """
    Function description

    Parameters
    ----------
    x : list of numbers
        description
    y : list of Shifts
        description

    Returns
    -------
    var1 : type
        description

    Example:
    --------
    >> a = func(x)
    """
    trace = go.Scatter(x=[shift.start_time for shift in x], y=y)
    xaxis = go.XAxis(
        showgrid=True,
        showline=True,
        showticklabels=True,
        ticktext=[str(shift.start_time) + f' Смена {shift.order}' for shift in x],
        tickvals=[shift.start_time for shift in x],
    )
    layout = go.Layout(
        title=title,
        xaxis=xaxis,
    )
    fig = go.Figure(data=[trace], layout=layout)
    return fig.to_plotly_json()


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = DeepDict(super().get_context_data(**kwargs))
        context.journal_title = 'Dashboard'
        context.menu_data = get_menu_data()
        return context


class DashboardConfigView(LoginRequiredMixin, View):
    @staticmethod
    def config2list(config):
        res = []
        for i in config:
            spec = config[i]
            spec["i"] = str(i)
            res.append(spec)
        return res

    @logged
    def get(self, request):
        employee = Employee.objects.get(user=request.user)
        dashboard_config = Setting.get_value(name="dashboard_config", employee=employee)
        if dashboard_config:
            return JsonResponse({"config": self.config2list(dashboard_config)})
        else:
            return JsonResponse({"config": {}})


class DashboardConfigUpdateView(LoginRequiredMixin, View):
    def post(self, request):
        layout = json.loads(request.body)
        employee = Employee.objects.get(user=request.user)
        config = Setting.get_value(name="dashboard_config", employee=employee)
        for item in layout:
            id = item["i"]
            for key in item:
                if key not in ["i", "moved"]:
                    config[id][key] = item[key]
        Setting.set_value(name="dashboard_config", employee=employee, value=config)
        return JsonResponse({"result": 1})


class GraphView(LoginRequiredMixin, View):
    @logged
    def post(self, request):
        field_id = json.loads(request.body)
        field = Field.objects.get(id=field_id)
        title = field.verbose_name if field.verbose_name else field.name
        y, x = get_data(field)
        print(x, y, title)
        graph = timeline(x, y, title)
        # print(dumps(graph, primitives=True))
        return HttpResponse(dumps(graph, primitives=True),
            content_type='application/json; charset=utf8')


class AddGraphView(View):
    @logged
    def post(self, request):
        user = request.user
        # user = User.objects.get(username="inframine")
        employee = Employee.objects.get(user=user)
        print(request.body)
        cell_info = json.loads(request.body)
        journal_name = cell_info["journal_name"]
        table_name = cell_info["table_name"]
        field_name = cell_info["field_name"]
        journal = Journal.objects.get(name=journal_name)
        table = Table.objects.get(name=table_name, journal_id=journal.id)
        field = Field.objects.get(name=field_name, table_id=table.id)

        dashboard_config = Setting.get_value(name="dashboard_config", employee=employee)
        if dashboard_config is None:
            dashboard_config = {}
        dashboard_config[str(field.id)] = dict(x=0, y=0, w=6, h=8)
        Setting.set_value(name="dashboard_config", employee=employee, value=dashboard_config)

        return JsonResponse({"result": 1})


class DeleteGraphView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        employee = Employee.objects.get(user=user)
        graph_id = json.loads(request.body)["id"]
        dashboard_config = Setting.get_value(name="dashboard_config", employee=employee)
        if graph_id in dashboard_config.keys():
            del dashboard_config[graph_id]
        Setting.set_value(name="dashboard_config", employee=employee, value=dashboard_config)
        return JsonResponse({"result": 1})
