from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'e_logs.core'
    verbose_name = 'Настройки'


from suit.apps import DjangoSuitConfig

class SuitConfig(DjangoSuitConfig):
    layout = 'vertical'