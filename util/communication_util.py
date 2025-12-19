from django.core.mail import EmailMessage, get_connection
from django.conf import settings

class CommunicationUtil:

    @staticmethod
    def email(email, subject, body, is_qchat = False):
        cfg = settings.EMAIL_ACCOUNTS["qchat" if is_qchat else "default"]

        connection = get_connection(
            host=cfg["HOST"],
            port=cfg["PORT"],
            username=cfg["USER"],
            password=cfg["PASSWORD"],
            use_tls=cfg["USE_TLS"],
        )

        msg = EmailMessage(
            subject=subject,
            body=body,
            from_email=cfg["USER"],
            to = [],
            bcc = email,
            connection=connection
        )

        msg.content_subtype = "html"
        msg.send()
