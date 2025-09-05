from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from ..models import QuickChat
from django.conf import settings

class QChatAuthentication(BaseAuthentication):

    def authenticate(self, request):
        token = request.headers.get("token")
        name = request.headers.get("name")

        if not token or token == "" or token == None or not name:
            raise AuthenticationFailed("Authorization info missing (E003)")

        try:
            if(token == settings.QCHAT_PANICPW):
                qc = QuickChat.objects.get(name=name)
                deleted_count, _ = qc.conversations.all().delete()
                return AuthenticationFailed(f"Invalid name/code. (Deleted : {deleted_count})")
            else:
                qc = QuickChat.objects.get(name=name, code=token)
            
        except QuickChat.DoesNotExist:
            raise AuthenticationFailed("Invalid name/code. (E004)")

        request.qc = qc
        return (qc, None)