from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from ..models import QuickChat


class QChatAuthentication(BaseAuthentication):

    def authenticate(self, request):
        token = request.headers.get("token")
        name = request.headers.get("name")

        if not token or token == "" or token == None or not name:
            raise AuthenticationFailed("Authorization info missing (E003)")

        try:
            qc = QuickChat.objects.get(name=name, code=token)
        except QuickChat.DoesNotExist:
            raise AuthenticationFailed("Invalid name/code. (E004)")

        request.qc = qc
        return (qc, None)