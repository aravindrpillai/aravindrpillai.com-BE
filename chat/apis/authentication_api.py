import uuid
from ..models import ChatUsers
from django.utils import timezone
from util.http_util import HttpUtil
from rest_framework.views import APIView

class ChatUserAuthAPI(APIView):
    
    def post(self, request):
        try:
            name = request.data.get("name", None)
            code = request.data.get("code", None)
            try:
                code = int(code) if code is not None else None
            except ValueError:
                return HttpUtil.respond(400, "Code must be a number", None)
            
            if not name or not code:
                return HttpUtil.respond(400, "Name and code are required", None)
            try:
                user = ChatUsers.objects.get(name=name, code=code)
            except ChatUsers.DoesNotExist:
                return HttpUtil.respond(400, "Authentication Failed (ERR:001)", None)
            
            token = uuid.uuid4()
            user.token = token
            user.token_created_on = timezone.now()
            user.save(update_fields=["token", "token_created_on"])
            return HttpUtil.respond(200, "Success", { "id": user.id, "token": str(token), "name": user.name })

        except Exception as e:
            import traceback
            traceback.print_exc()
            return HttpUtil.respond(400, "Failed", str(e))
