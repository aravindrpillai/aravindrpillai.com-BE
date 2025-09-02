from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from ..models import ChatUsers


class HeaderTokenAuthentication(BaseAuthentication):
    """
    Authenticate against `name` and `token` headers.
    """

    def authenticate(self, request):
        token = request.headers.get("token")
        name = request.headers.get("name")

        if not token or token == "" or token == None or not name:
            raise AuthenticationFailed("Authorization header missing (E003)")

        try:
            user = ChatUsers.objects.get(name=name, token=token)
        except ChatUsers.DoesNotExist:
            raise AuthenticationFailed("Invalid or expired token. (E004)")

        # DRF requires returning (user, auth)
        return (user, None)