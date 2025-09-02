from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError


class QchatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'qchat'

    def ready(self):
        from .models import QuickChat
        try:
            QuickChat.objects.get_or_create(name="marks", code=2808 )
            QuickChat.objects.get_or_create(name="chela", code=9001 )
            QuickChat.objects.get_or_create(name="res", code=1104 )
            QuickChat.objects.get_or_create(name="gop", code=2205 )

        except (OperationalError, ProgrammingError):
            # Happens before the first migration
            pass
