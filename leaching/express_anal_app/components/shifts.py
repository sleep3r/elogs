from leaching.express_anal_app.services.shifts import get_editable_shifts
from utils.webutils import process_json_view


@process_json_view(auth_required=False)
def accessible_shifts(request):
    emp = request.user.employee
    return get_editable_shifts(emp)