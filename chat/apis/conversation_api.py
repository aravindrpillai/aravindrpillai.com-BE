from django.db.models import Q
from ..models import Conversations, ChatUsers
from util.http_util import HttpUtil
from rest_framework.views import APIView
from chat.apis.api_base import HeaderTokenAuthentication

class ConversationAPI(APIView):
    
    authentication_classes = [HeaderTokenAuthentication]

    def get(self, request, recipient_name):
        try:
            lastid = int(request.query_params.get("lastid", 0))
            recipient = ChatUsers.objects.get(name=recipient_name)
            
            conversations = Conversations.objects.filter(
                Q(sender=request.user, recipient=recipient) |
                Q(sender=recipient, recipient=request.user),
                id__gt=lastid
            ).order_by("time")

            #Conversations.objects.filter(recipient=request.user, sender_id=recipient_id, read=False).update(read=True)
            return HttpUtil.respond(200, None, [c.data() for c in conversations])
        except Exception as e:
            print(str(e))
            return HttpUtil.respond(400, "Error", str(e))



    def post(self, request, recipient_name):
        try:
            message = request.data.get("message")
            recipient = ChatUsers.objects.get(name=recipient_name)
            if not message:
                return HttpUtil.respond(400, "message is required", str(e))
            conv = Conversations.objects.create(sender = request.user, recipient=recipient, message=message)
            return HttpUtil.respond(200, "Success", conv.data())
        except Exception as e:
            return HttpUtil.respond(400, "Error", str(e))
            


    def delete(self, request, recipient_id):
        try:
            sender = request.user
            
            if not recipient_id:
                return HttpUtil.respond(400, "recipient_id is required", None)

            deleted_count, _ = Conversations.objects.filter(
                Q(sender=sender, recipient_id=recipient_id) |
                Q(sender_id=recipient_id, recipient=sender)
            ).delete()

            return HttpUtil.respond(200, "Deleted :"+deleted_count, None)

        except Exception as e:
            HttpUtil.respond(400, "Error", str(e))
