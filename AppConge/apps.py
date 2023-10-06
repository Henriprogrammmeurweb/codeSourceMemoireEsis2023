from django.apps import AppConfig


class AppcongeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AppConge'
    def ready(self):
        import AppConge.signals
