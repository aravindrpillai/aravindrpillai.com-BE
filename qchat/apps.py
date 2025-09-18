from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError


class QchatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'qchat'

    def ready(self):
        from .models import QuickChat
        try:
            QuickChat.objects.get_or_create(name="test", code=1234 )

        except (OperationalError, ProgrammingError):
            # Happens before the first migration
            pass
