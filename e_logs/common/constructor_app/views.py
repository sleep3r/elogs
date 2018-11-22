import hashlib
import os
from datetime import timedelta

from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from proxy.views import proxy_view

from e_logs.common.all_journals_app.models import Shift
from e_logs.common.all_journals_app.services.journal_builder import JournalBuilder
from e_logs.core.management.commands.compress_journals import compress_journal
from django.views import View
from django.http import JsonResponse

from e_logs.core.models import Setting
from e_logs.core.utils.webutils import current_date, date_range


@csrf_exempt
def constructor_proxy(request, path):
    remoteurl = 'http://localhost:3000/' + path
    return proxy_view(request, remoteurl)


class ConstructorHashAPI(View):
    def post(self, request):
        journal = request.FILES['journal_file']

        fs = FileSystemStorage(location=f'resources/temp/')
        filename = fs.save(journal.name, journal)

        hasher = hashlib.md5()
        with open(f'resources/temp/{filename}', 'rb') as afile:
            buf = afile.read()
            hasher.update(buf)
        journal_hash = hasher.hexdigest()
        os.rename(f'resources/temp/{filename}', f'resources/temp/{journal_hash}.jrn')

        return JsonResponse({"hash": journal_hash})


class ConstructorUploadAPI(View):
    def post(self, request):
        print(request.POST)
        hash = request.POST.get('hash', None)
        plant = request.POST.get('plant', None)
        type = request.POST.get('type', None)
        number_of_shifts = request.POST.get('number_of_shifts', 2)

        if not hash or not plant:
            return JsonResponse({"status": 2, "message": "Couldnt upload without hash or plant"})

        journal = JournalBuilder(f'resources/temp/{hash}.jrn', plant, type)
        new_journal = journal.create()

        if new_journal.type == 'shift' and number_of_shifts:
            LoadJournalAPI.add_shifts(new_journal, int(number_of_shifts))

        compress_journal(new_journal)
        return JsonResponse({"status": 1})

class LoadJournalAPI(View):
    def post(self, request):
        if request.FILES.get('journal_file', None):
            journal = request.FILES['journal_file']
            plant_name = request.POST['plant']
            type = request.POST['type']
            number_of_shifts = int(request.POST['number_of_shifts'])
            if plant_name and type and number_of_shifts:
                try:
                    os.remove(f'resources/journals/{plant_name}/{journal.name}')
                except OSError:
                    pass
                fs = FileSystemStorage(location=f'resources/journals/{plant_name}/')
                filename = fs.save(journal.name, journal)

                journal = JournalBuilder(journal, plant_name, type)
                new_journal = journal.create()

                if new_journal.type == 'shift':
                    self.add_shifts(new_journal, number_of_shifts)

                return JsonResponse({"status": 1})
        return JsonResponse({"status": 0})

    @staticmethod
    def add_shifts(new_journal, number_of_shifts):
        Setting.of(obj=new_journal)['number_of_shifts'] = int(number_of_shifts)
        now_date = current_date()
        for shift_date in date_range(now_date - timedelta(days=7), now_date + timedelta(days=7)):
            for shift_order in range(1, number_of_shifts + 1):
                Shift.objects.get_or_create(journal=new_journal, order=shift_order, date=shift_date)
