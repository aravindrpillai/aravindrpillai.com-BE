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
            print(str(e))
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
            

    def delete(self, request):
        try:
            deleted_count, _ = request.qc.conversations.all().delete()
            return HttpUtil.respond(200, f"Deleted : {deleted_count}", None)
        except Exception as e:
            HttpUtil.respond(400, "Error", str(e))
