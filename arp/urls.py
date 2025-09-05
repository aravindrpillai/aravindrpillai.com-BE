from django.urls import path
from qchat.apis.qchatconv import QChatConvAPI
from anonymous.api import AnonymousAPI
from textbox.api import TextBoxAPI

urlpatterns = [
    #Quick Chat Conversations
    path("arp/qchat/conversations/", QChatConvAPI.as_view(), name="quick-chat-conversations"),

    #Anoymous
    path("arp/anonymous/", AnonymousAPI.as_view(), name="anonymous-messages"),

    #Textbox
    path("arp/textbox/<str:code>/", TextBoxAPI.as_view(), name="text-box-api"),
    
]
