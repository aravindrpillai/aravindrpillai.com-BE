from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
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
                decryptedCode = self.decrypt_from_react(token, str(qc.code))
                if str(qc.code) != decryptedCode:
                    raise AuthenticationFailed("Invalid name/code. (E004)")
        except QuickChat.DoesNotExist:
            raise AuthenticationFailed("Invalid name/code. (E005)")
        request.qc = qc
        return (qc, None)

    
    def decrypt_from_react(self, cipherdCode, code):
        IV = settings.QCHAT_ENCRYPTION_IV.encode("utf-8")
        key = hashlib.sha256(code.encode()).digest()
        raw = base64.b64decode(cipherdCode)
        cipher = AES.new(key, AES.MODE_CBC, IV)
        decrypted = cipher.decrypt(raw)
        pad_len = decrypted[-1]
        decrypted = decrypted[:-pad_len]
        return decrypted.decode("utf-8")
