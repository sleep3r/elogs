from django.views.decorators.csrf import csrf_exempt
from proxy.views import proxy_view
from e_logs.common.all_journals_app.services.journal_builder import JournalBuilder
from e_logs.core.management.commands.compress_journals import compress_journal
from django.core.files.storage import FileSystemStorage
from e_logs.common.all_journals_app.api.views import LoadJournalAPI
from django.views import View
from django.http import JsonResponse
import hashlib
import os


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