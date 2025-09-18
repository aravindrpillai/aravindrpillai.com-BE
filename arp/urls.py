from django.urls import path
from qchat.apis.qchatconv import QChatConvAPI
from qchat.apis.qchat_admin import QuickChatAdminAPI
from anonymous.api import AnonymousAPI
from textbox.api import TextBoxAPI

urlpatterns = [
    #Quick Chat Conversations
    path("arp/qchat/conversations/", QChatConvAPI.as_view(), name="quick-chat-conversations"),
    path("arp/qchat/admin/<str:name>/", QuickChatAdminAPI.as_view(), name="quick-chat-admin-api"),
    path("arp/qchat/admin/", QuickChatAdminAPI.as_view(), name="quick-chat-admin-api"),

    #Anoymous
    path("arp/anonymous/", AnonymousAPI.as_view(), name="anonymous-messages"),

    #Textbox
    path("arp/textbox/<str:code>/", TextBoxAPI.as_view(), name="text-box-api"),
    
]
