from django.apps import AppConfig

from .tasks import cleanup_sessions


class ShortyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.shorty'

    def ready(self):
        """
        Starting the periodic task of clearing expired sessions
        """
        cleanup_sessions()
