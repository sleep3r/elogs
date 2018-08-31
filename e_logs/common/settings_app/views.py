from django.shortcuts import render
from django.views.generic import TemplateView


class SettingsView(TemplateView):
    template_name = 'settings.html'
    # model = JsonTable
    # form = TableForms
    # json_form = JsonForm

    def post(self, request):
        pass


    def get_context_data(self, *args, **kwargs):
        pass