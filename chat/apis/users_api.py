from rest_framework.views import APIView
from django.db import IntegrityError
from ..models import ChatUsers
from util.http_util import HttpUtil

class ChatUserRegistrationAPI(APIView):
    
   

    def post(self, request):
        try:
            name = request.data.get("name")
            code = request.data.get("code")
            mob = request.data.get("mobile_number")
            msg = request.data.get("notification_msg")

            if not name or not code or len(name) < 4 or int(code) < 1000 or int(code) > 9999:
                return HttpUtil.respond(400, "A min 4 char name and a 4 digit code are required", None)

            user = ChatUsers.objects.create(name=name.lower(), code=code, mobile_number=mob, notification_msg=msg)
            return HttpUtil.respond(200, "Success", None)

        except IntegrityError:
            return HttpUtil.respond(400, "name already taken", None)
        except Exception as e:
            return HttpUtil.respond(400, "Failed", str(e))
