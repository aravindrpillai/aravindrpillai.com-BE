from django.db import models
from django.utils import timezone

class Anonymous(models.Model):

    message = models.TextField(max_length=4000, null=False)
    time = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=200, null=True, default=None)
    cordinates = models.CharField(max_length=100, null=True, default=None)
    ip = models.GenericIPAddressField(default=None, blank=True, null=True)
    isp = models.CharField(max_length=100, null=True, default=None)
    
    class Meta:
        db_table = "anonymous"

    def data(self):
        return {
            "id": self.id, 
            "message": self.message,
            "location": self.location, 
            "cordinates": self.cordinates, 
            "time" : self.time,
            "ip": self.ip,
            "isp": self.isp
        }
