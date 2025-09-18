from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class QuickChat(models.Model):
    name = models.CharField(max_length=10, null=False, unique=True)
    code = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(9999)], null=False)
    
    class Meta:
        db_table = "qc_chat"

class Conversations(models.Model):
    qchat = models.ForeignKey(QuickChat, related_name="conversations",on_delete=models.CASCADE)
    sender = models.CharField(max_length=10, null=False)
    message = models.TextField(max_length=2000, null=False)
    time = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = "qc_conversations"

    def data(self):
        return {
            "id": self.id, 
            "name": self.qchat.name,
            "sender": self.sender, 
            "time" : self.time,
            "message": self.message
        }
