from django.apps import AppConfig


class CommonAllJournalsAppConfig(AppConfig):
    name = 'e_logs.common.all_journals_app'
    verbose_name = 'Все журналы'

    def ready(self):
        import e_logs.common.all_journals_app.signals
