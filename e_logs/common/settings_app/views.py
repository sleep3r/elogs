from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView
from e_logs.common.all_journals_app.services.context_creator import get_context


class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'settings.html'
    # model = JsonTable
    # form = TableForms
    # json_form = JsonForm

    def post(self, request):
        pass

    def get_context_data(self, *args, **kwargs):
        context = get_context(self.request, page=None)
        return  context