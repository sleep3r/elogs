from django.shortcuts import render

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from utils.deep_dict import deep_dict

# Create your views here.
from django.template import loader

# from common.all_journals_app.models import JournalPage
# from common.all_journals_app.services.context_creator import get_common_context


@login_required
def index(request):
    context = {}
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))
