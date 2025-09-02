from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class ChatUsers(models.Model):
    name = models.CharField(max_length=20, unique=True)
    code = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(9999)])
    mobile_number = models.CharField(max_length=14, default=None, null=True)
    notification_msg = models.CharField(max_length=200, default=None, null=True)
    token = models.UUIDField(unique=True, null=True, blank=True)
    token_created_on = models.DateTimeField(null=True, blank=True)


class Conversations(models.Model):
    sender = models.ForeignKey(ChatUsers, related_name="sender",on_delete=models.CASCADE)
    recipient = models.ForeignKey(ChatUsers, related_name="recipient", on_delete=models.CASCADE)
    message = models.TextField(max_length=2000)
    time = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)

    def data(self):
        return {
            "id": self.id, 
            "sender": self.sender.name, 
            "recipient": self.recipient.name, 
            "message" : self.message, 
            "time": self.time.isoformat(), 
            "read": self.read 
        }
