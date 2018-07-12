from django.db import transaction
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.template import loader, TemplateDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from login_app.models import Employee

from common.all_journals_app.fields_descriptions.fields_info import fields_info_desc
from common.all_journals_app.models import CellValue, JournalPage
from utils.webutils import process_json_view
from common.messages_app.services import messages
from .feedback import feedback


@csrf_exempt
@process_json_view(auth_required=False)
def change_table(request):
    tn = request.POST['table_name']
    jp = request.POST['journal_page']

    page = JournalPage.objects.get(id=int(jp))

    employee = request.user.employee
    page.employee_set.add(employee)

    CellValue.objects.filter(table_name=tn, journal_page=page).delete()

    for field_name in request.POST:
        values = request.POST.getlist(field_name)
        for i, val in enumerate(values):
            CellValue(journal_page=page, value=val, index=i, field_name=field_name, table_name=tn).save()

    return {"status": 1}


@csrf_exempt
@process_json_view(auth_required=False)
def get_fields_descriptions(request):
    return fields_info_desc


@csrf_exempt
@process_json_view(auth_required=False)
def add_responsible(request):
    table_name = request.POST.get('table_name', None)
    field_name = request.POST.get('field_name', None)
    row_index = request.POST.get('index', None)
    journal_page = request.POST.get('journal_page', None)

    cell = messages.get_or_none(CellValue, journal_page = journal_page, table_name = table_name, index = row_index, field_name = field_name)

    if cell:
        cell.responsible = request.user.employee
        cell.save()

    return {"result":1}


def permission_denied(request, exception, template_name='errors/403.html'):
    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        return HttpResponseForbidden('<h1>403 Forbidden</h1>', content_type='text/html')
    return HttpResponseForbidden(
        template.render(request=request, context={'exception': str(exception)}))

@csrf_exempt
@process_json_view(auth_required=False)
def send_message_to_devs(request):
    feedback(request.POST)
    return {"result":1}
