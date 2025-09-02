from django.contrib import admin
from django.urls import path
from chat.apis.users_api import ChatUserRegistrationAPI
from chat.apis.authentication_api import ChatUserAuthAPI
from chat.apis.conversation_api import ConversationAPI
from chat.apis.recipients_api import RecipientsAPI
from qchat.apis.qchatconv import QChatConvAPI

urlpatterns = [
    path('admin/', admin.site.urls),

    path("arp/chat/users/register/", ChatUserRegistrationAPI.as_view(), name="chat-user-registration"),
    path("arp/chat/users/auth/", ChatUserAuthAPI.as_view(), name="chat-user-authentication"),
    path("arp/chat/conv/recipients/", RecipientsAPI.as_view(), name="chat-user-recipients"),
    path("arp/chat/conv/<str:recipient_name>/", ConversationAPI.as_view(), name="chat-conversation-addition"),
   
    #Quick Chat Conversations
    path("arp/qchat/conversations/", QChatConvAPI.as_view(), name="quick-chat-conversations"),
    
]
