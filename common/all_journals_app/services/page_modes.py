from login_app.models import Employee
from django.core.exceptions import PermissionDenied

APP = 'all_journals_app'
VALIDATE_CELLS = APP + ".validate_cells"
EDIT_CELLS = APP + ".edit_cells"
VIEW_CELLS = APP + ".view_cells"
PLANT_PERM = APP + ".modify_{plant}"

class PageModeError(Exception):
    def __init__(self, value):
        self.value = value


def plant_permission(request):
    employee = Employee.objects.get(user=request.user)
    plant = request.path.split("/")[1]
    return employee.user.has_perm(PLANT_PERM.format(plant=plant))

def page_mode_is_valid(request, page):
    employee = Employee.objects.get(user=request.user)
    page_mode = request.GET.get('page_mode')
    if page_mode:
        if request.user.is_superuser:
                return True
        if plant_permission(request):
            if page_mode == "validate":
                return employee.user.has_perm(VALIDATE_CELLS)
            if page_mode == "edit":
                if page.type == "shift":
                    return page.shift_is_active and employee.user.has_perm(EDIT_CELLS)
                if page.type == "equipment":
                    return employee.user.has_perm(EDIT_CELLS)
            if page_mode == "view":
                return employee.user.has_perm(VIEW_CELLS)
        else:
            return page_mode == "view"
    else:
        return False

def has_edited(request, page):
    return page in request.user.employee.owned_journal_pages.all();


def default_page_mode(request, page):
    employee = Employee.objects.get(user=request.user)
    if plant_permission(request):
        if employee.user.has_perm(VALIDATE_CELLS):
            return "validate"
        elif employee.user.has_perm(VIEW_CELLS):
            return "view"
        else:
            raise PermissionDenied("Вам нечего делать на этой странице. Уходите.")
    else:
        if employee.user.has_perm(VIEW_CELLS):
            return "view"
        else:
            raise PermissionDenied("У вас нет доступа к этому цеху.")

def get_page_mode(request, page):
    if page_mode_is_valid(request, page):
        return request.GET.get('page_mode')
    else:
        return default_page_mode(request, page)
