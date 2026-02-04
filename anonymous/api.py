from .models import Anonymous
from util.http_util import HttpUtil
from rest_framework.views import APIView
from util.request_util import RequestInfo
from .auth import AnonymousChatAuthentication
from util.communication_util import CommunicationUtil

class AnonymousAPI(APIView):
    
    authentication_classes = [AnonymousChatAuthentication]

    def get(self, request):
        try:
            anonymous = Anonymous.objects.all()
            return HttpUtil.respond(200, None, [c.data() for c in anonymous])
        except Exception as e:
            return HttpUtil.respond(400, "Error", str(e))

    def post(self, request):
        try:
            message = request.data.get("message", None)
            if not message:
                return HttpUtil.respond(400, "invalid message", str(e))
            loc_info = RequestInfo(request).get_location_info()
            Anonymous.objects.create(
                message=message,
                location=loc_info.get("city"),
                cordinates=loc_info.get("cordinates"),
                ip=loc_info.get("ip"),
                isp=loc_info.get("isp"),
            )

            CommunicationUtil.email(["aravindrpillai1992@gmail.com"], "Anonymous Notification", None, False)
            return HttpUtil.respond(200, "Success", None)
        except Exception as e:
            return HttpUtil.respond(400, "Error", str(e))
        
    def delete(self, request):
        try:
            id = request.query_params.get("id", 0)
            if(not id or id == 0):
                return HttpUtil.respond(400, f"Failed to delete. Provide correct id", None)
            deleted_count, _ = Anonymous.objects.get(id=id).delete()
            return HttpUtil.respond(200, f"Deleted : {deleted_count}", None)
        except Exception as e:
            HttpUtil.respond(400, "Error", str(e))
