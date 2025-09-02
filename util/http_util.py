from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList
from rest_framework.exceptions import ErrorDetail
from rest_framework.response import Response
from rest_framework.views import APIView


class HttpUtil():

    @staticmethod
    def respond(response_code, messages, data = None):
        if isinstance(messages, Exception):
            messages = HttpUtil.extract_exception_message(messages)
        if isinstance(messages, ReturnDict):
            messages = HttpUtil.convert_message_from_serialiser(messages)
        elif(messages != None):
            if(hasattr(messages, '__len__') and (not isinstance(messages, str))):
                pass
            else:
                messages = [messages]
        dict = {
            'status' : True if response_code<300 else False
        }
        if(messages != None and len(messages)>0):
            dict['messages'] = messages
        if(data != None):
            dict['data'] = data
    
        #status.HTTP_201_CREATED
        return Response(dict, response_code)

    
    @staticmethod
    def extract_exception_message(exc):
        def flatten_errors(errors):
            if isinstance(errors, (list, tuple, ReturnList)):
                return [str(e) for e in errors]
            elif isinstance(errors, (dict, ReturnDict)):
                flat = []
                for field, value in errors.items():
                    if isinstance(value, (list, tuple)):
                        for v in value:
                            flat.append(f"{field}: {str(v)}")
                    else:
                        flat.append(f"{field}: {str(value)}")
                return flat
            elif isinstance(errors, ErrorDetail):
                return [str(errors)]
            else:
                return [str(errors)]

        if hasattr(exc, 'detail'):
            return flatten_errors(exc.detail)
        elif hasattr(exc, 'message_dict'):
            return flatten_errors(exc.message_dict)
        elif hasattr(exc, 'messages'):
            return flatten_errors(exc.messages)
        else:
            return [str(exc)]

    @staticmethod
    def convert_message_from_serialiser(errors):
        messages = []
        for field, error_list in errors.items():
            if isinstance(error_list, (list, ReturnList)):
                messages.extend(error_list)
            elif isinstance(error_list, (dict, ReturnDict)):
                messages.extend(HttpUtil.convert_message_from_serialiser(error_list))
        return messages