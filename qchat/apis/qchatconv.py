from ..models import Conversations
from util.http_util import HttpUtil
from rest_framework.views import APIView
from qchat.apis.qchat_auth import QChatAuthentication

class QChatConvAPI(APIView):
    
    authentication_classes = [QChatAuthentication]

    def get(self, request):
        try:
            lastid = request.query_params.get("lastid", 0)
            convs = request.user.conversations.filter(id__gt=lastid).order_by("id")
            return HttpUtil.respond(200, None, [c.data() for c in convs])
        except Exception as e:
            return HttpUtil.respond(400, "Error", str(e))

    def post(self, request):
        try:
            message = request.data.get("message", None)
            sender = request.data.get("sender", None)

            if not message or not sender:
                return HttpUtil.respond(400, "invalid message/sender", str(e))
            conv = Conversations.objects.create(qchat = request.qc, sender=sender.lower(), message=message)
            return HttpUtil.respond(200, "Success", conv.data())
        except Exception as e:
            return HttpUtil.respond(400, "Error", str(e))

    def put(self, request):
        try:
            from django.utils import timezone
            from datetime import timedelta
            from ..models import QuickChat
            from util.communication_util import CommunicationUtil
            from util.encryption import Encryption

            token = request.headers.get("token")
            name = request.headers.get("name")

            qc = QuickChat.objects.get(name=name)
            Encryption.decrypt(token, str(qc.code))  # will raise exception if invalid
            now = timezone.now()

            # -------- RATE LIMIT CHECK (1 HOUR) --------
            if qc.last_email_time:
                diff = now - qc.last_email_time
                if diff < timedelta(hours=2):
                    return HttpUtil.respond(429, "Last notification didn’t complete 2 hours", None)

            # -------- SEND EMAIL --------
            if qc.emails and len(qc.emails) > 0:
                subject = f"Grab your free coupons before they run out : {name}"
                CommunicationUtil.email(qc.emails, subject, None, True)
                qc.last_email_time = now
                qc.save(update_fields=["last_email_time"])

            return HttpUtil.respond(200, "Success", None)

        except Exception as e:
            return HttpUtil.respond(400, "Error", str(e))

                

    def delete(self, request):
        try:
            deleted_count, _ = request.qc.conversations.all().delete()
            request.qc.incorrect_pw_count = 0
            request.qc.save()
            return HttpUtil.respond(200, f"Deleted : {deleted_count}", None)
        except Exception as e:
            HttpUtil.respond(400, "Error", str(e))
