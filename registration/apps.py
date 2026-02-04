from django.apps import AppConfig


class RegistrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'registration'

    def ready(self):
        # Ensure social account signals are registered
        from . import signals  # noqa: F401
