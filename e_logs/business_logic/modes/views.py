from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from e_logs.business_logic.services import SetMode
from e_logs.common.all_journals_app.services.context_creator import get_context
from e_logs.common.login_app.models import Employee


@csrf_exempt
def create_mode(request):
    if request.method == 'GET':# POST
    #     data = json.loads(request.body)
    #     data['sendee'] = request.user.employee
    #     SetMode.execute(**data)
    #     return JsonResponce({"status":1})
    #
        SetMode.execute({"beginning":timezone.now(),
            "end":timezone.now() + timedelta(minutes=3),
            "journal_id":16,
            "table_name": "big",
            "message":"12345",
            'sendee':Employee.objects.get(name='inframine'),
            "fields":[
                {"name":"wagon_num","min_normal":228, "max_normal":1488},
            ]})

        return JsonResponse({"status":1})

class ModeView(LoginRequiredMixin, TemplateView):
    template_name = 'modes.html'
    # model = JsonTable
    # form = TableForms
    # json_form = JsonForm

    def post(self, request):
        pass

    def get_context_data(self, *args, **kwargs):
        context = get_context(self.request, page=None)
        return context
