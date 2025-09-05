from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

class AnonymousChatAuthentication(BaseAuthentication):

    def authenticate(self, request):
        try:
            if request.method in ["GET", "DELETE"]:
                token = request.headers.get("token")
                if token != settings.ANONYMOUS_PW:
                    raise AuthenticationFailed("Anonymous Authorization info missing (E003)")
            else:
                #For post no auth required
                pass
        except:
            raise AuthenticationFailed("Anonymous Authorization failed (E004)")

        return (None, None)