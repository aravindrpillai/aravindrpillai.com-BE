from django.conf import settings
from Crypto.Cipher import AES
import base64, hashlib

class Encryption:

    IV_STR = settings.QCHAT_ENCRYPTION_IV
    
    @staticmethod
    def decrypt(encrypted_text :str, key : str) -> str:
        encrypted_text = str(encrypted_text)
        key = str(key)
        IV = Encryption.IV_STR.encode("utf-8")
        key = hashlib.sha256(key.encode()).digest()
        raw = base64.b64decode(encrypted_text)
        cipher = AES.new(key, AES.MODE_CBC, IV)
        decrypted = cipher.decrypt(raw)
        pad_len = decrypted[-1]
        decrypted = decrypted[:-pad_len]
        return decrypted.decode("utf-8")

    @staticmethod
    def encrypt(plain_text :str, key : str) -> str:
        plain_text = str(plain_text)
        key = str(key)
        IV = Encryption.IV_STR.encode("utf-8")
        key = hashlib.sha256(key.encode()).digest()
        data = plain_text.encode("utf-8")
        pad_len = AES.block_size - (len(data) % AES.block_size)
        padded_data = data + bytes([pad_len] * pad_len)
        cipher = AES.new(key, AES.MODE_CBC, IV)
        encrypted = cipher.encrypt(padded_data)
        return base64.b64encode(encrypted).decode("utf-8")
    
