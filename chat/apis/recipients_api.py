from ..models import Conversations, ChatUsers
from util.http_util import HttpUtil
from rest_framework.views import APIView
from chat.apis.api_base import HeaderTokenAuthentication

class RecipientsAPI(APIView):
    authentication_classes = [HeaderTokenAuthentication]
    
    
    def get(self, request):
        try:
            sent_to = Conversations.objects.filter(sender=request.user).values_list("recipient", flat=True)
            received_from = Conversations.objects.filter(recipient=request.user).values_list("sender", flat=True)
            partner_ids = set(sent_to) | set(received_from)

            partners = ChatUsers.objects.filter(id__in=partner_ids).exclude(id=request.user.id)

            respData = [{
                "id" : p.id,
                "name" : p.name,
                "unread_msgs" : Conversations.objects.filter(sender=p, recipient=request.user,read=False).count()
            } for p in partners]

            return HttpUtil.respond(200, None, respData)
        except Exception as e:
            print(str(e))
            return HttpUtil.respond(400, "Recipients Error", str(e))