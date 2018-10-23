from django.apps import AppConfig
from suit.apps import DjangoSuitConfig


class CoreConfig(AppConfig):
    name = 'e_logs.core'
    verbose_name = 'Основные элементы системы'


class SuitConfig(DjangoSuitConfig):
    layout = 'vertical'