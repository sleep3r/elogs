from django.shortcuts import render
from django.views.generic import TemplateView
from e_logs.common.all_journals_app.services.context_creator import get_context


class SettingsView(TemplateView):
    template_name = 'settings.html'
    # model = JsonTable
    # form = TableForms
    # json_form = JsonForm

    def post(self, request):
        pass


    def get_context_data(self, *args, **kwargs):
        context = get_context(self.request, plant=None, journal=None)
        return  context