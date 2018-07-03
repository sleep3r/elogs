from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from login_app.models import Employee

from common.all_journals_app.fields_descriptions.fields_info import fields_info_desc
from common.all_journals_app.models import CellValue, JournalPage
from utils.webutils import process_json_view
from common.messages_app.services import messages



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
            CellValue(journal_page=page, value=val, index=i, field_name=field_name, table_name=tn, responsible=request.user.employee).save()
    
    return {"status": 1}


@csrf_exempt
@process_json_view(auth_required=False)
def get_fields_descriptions(request):
    return fields_info_desc
