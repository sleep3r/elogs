from django.contrib.auth.models import User

from login_app.models import Employee


def add_user(user_dict):
    user_name = (user_dict['en']['last_name']
                + "-" + user_dict['en']['first_name']
                + "-" + user_dict['en']['second_name']).strip('-')


    if User.objects.filter(username=user_name).exists():
        print(f'user `{user_name}` already exists')
    else:
        user = User.objects.create_user(user_name, password='qwerty')
        user.first_name = user_dict['ru']['first_name']
        user.last_name = user_dict['ru']['last_name']
        user.is_superuser = False
        user.is_staff = True
        user.save()

        # emplyee = Employee()
        # emplyee.user = user
        # emplyee.position =
        #
        #
        # user.id


def add_groups(user_groups):

    for key, group_name in user_groups.items():
        if Group.objects.filter(name=group_name).exists():
            print(f'Group `{group_name}` already exists')
        else:
            print(f'{key}->{group_name}')
            group_name = user_groups[key]
            group = Group.objects.create(name=group_name)
            group.save()
    print("Groups added")

def set_permissions_for_groups():
    print("Set permissions for groups")