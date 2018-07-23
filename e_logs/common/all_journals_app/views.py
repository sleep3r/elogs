from django.db import transaction
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.template import loader, TemplateDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from e_logs.common.login_app.models import Employee

from e_logs.common.all_journals_app.fields_descriptions.fields_info import fields_info_desc
from e_logs.common.all_journals_app.models import CellValue, JournalPage, Feedback
from e_logs.core.utils.webutils import process_json_view, logged
from e_logs.common.messages_app.services import messages
from .feedback import send_feedback


@csrf_exempt
@process_json_view(auth_required=False)
@logged
def change_table(request):
    tn = request.POST['table_name']
    jp = request.POST['journal_page']

    page = JournalPage.objects.get(id=int(jp))

    employee = request.user.employee
    page.employee_set.add(employee)

    CellValue.objects.filter(table_name=tn, journal_page=page).delete()

    for field_name in request.POST:
        values = request.POST.getlist(field_name)
        with transaction.atomic():
            for i, val in enumerate(values):
                CellValue(journal_page=page, value=val, index=i, field_name=field_name, table_name=tn).save()

    return {"status": 1}


@csrf_exempt
@process_json_view(auth_required=False)
@logged
def get_fields_descriptions(request):
    return fields_info_desc


@logged
def permission_denied(request, exception, template_name='errors/403.html'):
    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        return HttpResponseForbidden('<h1>403 Forbidden</h1>', content_type='text/html')
    return HttpResponseForbidden(
        template.render(request=request, context={'exception': str(exception)}))

@csrf_exempt
@process_json_view(auth_required=False)
@logged
def send_message_to_devs(request):
    send_feedback(request.POST)
    return {"result":1}
