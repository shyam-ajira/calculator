from django.apps import AppConfig


class AjiraConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ajira'

    def ready(self):
        import ajira.signals