from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from common.all_journals_app.models import CellValue, JournalPage
from utils.webutils import process_json_view


@csrf_exempt
@process_json_view(auth_required=False)
def change_table(request):
    tn = request.POST['table_name']
    jp = request.POST['journal_page']

    page = JournalPage.objects.get(id=int(jp))

    CellValue.objects.filter(table_name=tn, journal_page=page).delete()

    for field_name in request.POST:
        values = request.POST.getlist(field_name)
        for i, val in enumerate(values):
            index = i if len(values) > 1 else None
            CellValue(journal_page=page, value=val, index=index, field_name=field_name, table_name=tn).save()

    return {"status": 1}