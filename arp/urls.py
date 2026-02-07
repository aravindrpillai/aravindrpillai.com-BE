from django.urls import path
from qchat.apis.qchatconv import QChatConvAPI
from qchat.apis.qchat_admin import QuickChatAdminAPI
from anonymous.api import AnonymousAPI
from textbox.api import TextBoxAPI
from django.http import JsonResponse
from django.views import View

class PingAPI(View):
    def get(self, request):
        try:
            from util.communication_util import CommunicationUtil
            CommunicationUtil.email(["aravind.ramachandran.pillai@gmail.com"], "App is up and running","<EOM>")
            return JsonResponse({"status": "ok", "message": "App is up and running" })
        except Exception as e:
            return JsonResponse({"status": "ok", "message": f"App is up and running - but email failed : {str(e)}" })

urlpatterns = [
    path("ping/", PingAPI.as_view(), name="ping"),

    #Quick Chat Conversations
    path("arp/qchat/conversations/", QChatConvAPI.as_view(), name="quick-chat-conversations"),
    path("arp/qchat/conversations/delete/<int:conversation_id>/", QChatConvAPI.as_view(), name="quick-chat-conversations-delete"),
    path("arp/qchat/admin/", QuickChatAdminAPI.as_view(), name="quick-chat-admin-api"),

    #Anoymous
    path("arp/anonymous/", AnonymousAPI.as_view(), name="anonymous-messages"),

    #Textbox
    path("arp/textbox/<str:code>/", TextBoxAPI.as_view(), name="text-box-api"),
    
]
