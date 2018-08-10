from django.contrib.auth.models import User, Group, Permission
from e_logs.common.login_app.models import Employee
from loggers import err_logger


def add_user(user_dict):
    user_name = (user_dict['en']['last_name']
                 + "-" + user_dict['en']['first_name']
                 + "-" + user_dict['en']['second_name']).strip('-')

    if User.objects.filter(username=user_name).exists():
        err_logger.warning(f'user `{user_name}` already exists')
        return 0
    else:
        user = User.objects.create_user(user_name, password='qwerty')
        user.first_name = user_dict['ru']['first_name']
        user.last_name = user_dict['ru']['last_name']
        user.is_superuser = False
        user.is_staff = True
        for group in user_dict["groups"]:
            user.groups.add(Group.objects.get(name=group))
        user.user_permissions.add(Permission.objects.get(codename="view_cells"))

        e = Employee()
        e.name = user.first_name + ' ' + user.last_name
        e.position = user_dict["groups"][0].lower()
        e.plant = user_dict["groups"][1].lower()
        e.user = user

        e.save()

        user.save()
        return user.id
