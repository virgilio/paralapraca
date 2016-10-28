from django.apps import AppConfig


class ParalapracaConfig(AppConfig):
    name = 'paralapraca'
    verbose_name = 'Paralapraca'

    def ready(self):
        import paralapraca.signals
