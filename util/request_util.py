import requests

class RequestInfo:
    def __init__(self, request):
        self.request = request

    def get_ip(self):
        x_forwarded_for = self.request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = self.request.META.get("REMOTE_ADDR")
        return ip

    def get_location_info(self):
        try:
            ip = self.get_ip()
            url = f"http://ip-api.com/json/{ip}"
            response = requests.get(url, timeout=10).json()
            print(response)
            if response.get("status") == "success":
                return {
                    "ip": ip,
                    "city": f"{response.get('city')}, {response.get('regionName')}, {response.get('country')}",
                    "cordinates": f"{response.get('lat')},{response.get("lon")}",
                    "isp": response.get("isp")
                }
            else:
                raise Exception(response["message"])
        except Exception as e:
            return {
                "ip": ip,
                "city": f"Error : {str(e)}",
                "cordinates": "0.00,0.00",
                "isp": "nil"
            }
        