from django.contrib.auth.models import User

def add_user(user_dict):
    user_name = user_dict['en']['last_name'] \
                + "-" + user_dict['en']['first_name'] \
                + "-" + user_dict['en']['second_name']
    user = User.objects.create_user(user_name, password='qwerty')
    user.first_name = user_dict['ru']['first_name']
    user.last_name = user_dict['ru']['last_name']
    user.is_superuser = False
    user.is_staff = True
    user.save()



