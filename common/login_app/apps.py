from django.apps import AppConfig


class CommonLoginApp(AppConfig):
    name = 'common.login_app'
    verbose_name = 'Рабочие'

    def ready(self):
        from django.contrib.auth.models import User
        from common.login_app.models import Employee

        if not User.objects.filter(username='inframine'):
            print('Created superuser')
            u = User.objects.create_superuser("inframine", "admin@admin.com", "Singapore2017")
            u.save()

            # u.employee = Employee()
            # u.employee.name = 'The God'
            # u.employee.csfr = 'dsfh234iys734'
            # u.employee.plant = "leaching"
            # u.employee.position = "admin"

            # u.employee.save()
            # u.save()
