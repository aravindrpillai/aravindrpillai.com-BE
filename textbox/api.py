from .models import Textbox
from util.http_util import HttpUtil
from rest_framework.views import APIView

class TextBoxAPI(APIView):
    
    def get(self, request, code):
        if not code:
            return HttpUtil.respond(400, "Invalid Code", None)
        else:
            code = code.lower()
        tb, created = Textbox.objects.get_or_create(code=code)
        return HttpUtil.respond(200, None, tb.content)


    def post(self, request, code):
        if not code:
            return HttpUtil.respond(400, "Invalid Code", None)
        else:
            code = code.lower()
        tb, created = Textbox.objects.get_or_create(code=code)
        content = request.data.get("content", None)
        tb.content = content
        tb.save()
        return HttpUtil.respond(200, "Success", None)
    
    
    def delete(self, request, code=None):
        Textbox.objects.all().delete()
        return HttpUtil.respond(200, "Success", None)
    
    