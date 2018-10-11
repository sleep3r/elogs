from e_logs.business_logic import services
from e_logs.common.login_app.models import Employee
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

from e_logs.core.models import Setting

APP = 'all_journals_app'
VALIDATE_CELLS = APP + ".validate_cells"
EDIT_CELLS = APP + ".edit_cells"
VIEW_CELLS = APP + ".view_cells"
PLANT_PERM = APP + ".modify_{plant}"


#@login_required
def plant_permission(user, plant):
    employee = Employee.objects.get(user=user)
    return user.has_perm(PLANT_PERM.format(plant=plant))


@login_required
def page_mode_is_valid(request, page) -> bool:
    employee = Employee.objects.get(user=request.user)
    page_mode = request.GET.get('page_mode')
    if not page_mode:
        return False

    user_groups = [g.name for g in request.user.groups.all()]
    is_valid = request.user.is_superuser or {"Boss", page.journal.plant.name.title()}.\
             issubset(set(user_groups)) or "Big boss" in user_groups

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
        if page.journal.type == "shift" or page.journal.type == "equipment":
            is_valid = not page.closed and employee.user.has_perm(EDIT_CELLS) and not page.ended
            if page.closed:
                limited_emp_id_list = Setting.of(page)["limited_access_employee_id_list"]
                if limited_emp_id_list and employee.id in limited_emp_id_list:
                    is_valid = True

    if page_mode == "view":
        is_valid = employee.user.has_perm(VIEW_CELLS)
    return is_valid


@login_required
def has_edited(request, page) -> bool:
    return page in list(request.user.employee.shift_set.all())


#@login_required
def get_page_mode(user, plant) -> str:
    employee = Employee.objects.get(user=user)
    if plant_permission(user, plant):
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
