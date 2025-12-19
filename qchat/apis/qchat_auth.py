from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from util.encryption import Encryption
from django.conf import settings
from ..models import QuickChat
from Crypto.Cipher import AES
import base64, hashlib


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
                qc = QuickChat.objects.get(name=name)
                if(qc.incorrect_pw_count > 4):
                    deleted_count, _ = qc.conversations.all().delete()
                    raise AuthenticationFailed("Locked. (E004)")
                
                #If in debug mode, we can pass plain code, else emcrypted token is required
                if settings.DEBUG:
                    token = Encryption.encrypt(token, str(qc.code))
                
                decryptedCode = Encryption.decrypt(token, str(qc.code))
                if str(qc.code) != decryptedCode:
                    qc.incorrect_pw_count = (qc.incorrect_pw_count + 1)
                    qc.save()
                    raise AuthenticationFailed("Invalid name/code. (E005)")
                
        except QuickChat.DoesNotExist:
            raise AuthenticationFailed("Invalid name/code. (E006)")
        except Exception:
            raise AuthenticationFailed("Invalid token code")
        request.qc = qc
        return (qc, None)