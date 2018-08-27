from e_logs.business_logic.modes import services
from e_logs.common.login_app.models import Employee
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

APP = 'all_journals_app'
VALIDATE_CELLS = APP + ".validate_cells"
EDIT_CELLS = APP + ".edit_cells"
VIEW_CELLS = APP + ".view_cells"
PLANT_PERM = APP + ".modify_{plant}"


@login_required
def plant_permission(request):
    employee = Employee.objects.get(user=request.user)
    plant = request.path.split("/")[1]
    return employee.user.has_perm(PLANT_PERM.format(plant=plant))


@login_required
def page_mode_is_valid(request, page) -> bool:
    employee = Employee.objects.get(user=request.user)
    page_mode = request.GET.get('page_mode')
    if not page_mode:
        return False

    is_valid = request.user.is_superuser or \
         {"Boss", page.journal.plant.name.title()}.\
             issubset(set([g.name for g in request.user.groups.all()]))


    if plant_permission(request):
        has_perm = check_mode_permissions(employee, page, page_mode)
        if has_perm == True:
            has_perm = services.CheckRole.execute({"employee":request.user.employee, "page":page}) \
            and services.CheckTime.execute({"employee": request.user.employee, "page": page})
    else:
        has_perm = page_mode == "view"

    return has_perm or is_valid


@login_required
def check_mode_permissions(employee: Employee, page, page_mode: str) -> bool:
    is_valid = False
    if page_mode == "validate":
        is_valid = employee.user.has_perm(VALIDATE_CELLS)
    if page_mode == "edit":
        if page.journal.type == "shift":
            is_valid = page.is_active and employee.user.has_perm(EDIT_CELLS)
        if page.journal.type == "equipment":
            is_valid = employee.user.has_perm(EDIT_CELLS)
    if page_mode == "view":
        is_valid = employee.user.has_perm(VIEW_CELLS)
    return is_valid


@login_required
def has_edited(request, page) -> bool:
    return page in list(request.user.employee.owned_shifts.all())


@login_required
def default_page_mode(request) -> str:
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


@login_required
def get_page_mode(request, page) -> str:
    if page_mode_is_valid(request, page):
        return request.GET.get('page_mode')
    else:
        return default_page_mode(request)
