from rest_framework.exceptions import AuthenticationFailed
from util.http_util import HttpUtil
from rest_framework.views import APIView
from ..models import QuickChat
from django.conf import settings

class QuickChatAdminAPI(APIView):
    
    def dispatch(self, request, *args, **kwargs):
        token = request.headers.get("token")
        if token != settings.QCHAT_ADMIN_PW:
            raise AuthenticationFailed("Authorization info missing (E003)")
        return super().dispatch(request, *args, **kwargs)
    

    def post(self, request):
        try:
            data = request.data
            name = data.get("name")
            code = data.get("code")
            if not name or not code:
                return HttpUtil.respond(400, "Both 'name' and 'code' are required", None)
            if QuickChat.objects.filter(name=name).exists():
                return HttpUtil.respond(400, "Record with this name already exists", None)
            QuickChat.objects.create(name=name, code=int(code))
            return HttpUtil.respond(200, "Record created successfully")
        except Exception as e:
            return HttpUtil.respond(400, "Failed to add", e)

        
    # Update
    def put(self, request, name):
        try:
            data = request.data
            code = data.get("code")

            chat = QuickChat.objects.get(name=name)
            deleted_count, _ = chat.conversations.all().delete()
                
            if code:
                chat.code = int(code)
                chat.incorrect_pw_count = 0
                chat.save()
            return HttpUtil.respond(200, "Code Updated Successfully")
        except Exception as e:
            return HttpUtil.respond(400, "Failed to update", e)

    
    # Delete
    def delete(self, request, name):
        try:
            chat = QuickChat.objects.get(name=name)
            deleted_count, _ = chat.conversations.all().delete()
            chat.delete()
            return HttpUtil.respond(200, "Record deleted successfully")
        except Exception as e:
            return HttpUtil.respond(400, "Failed to delete", e)
