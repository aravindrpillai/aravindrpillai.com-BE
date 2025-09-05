from django.db import models

class Textbox(models.Model):

    code = models.TextField(null=False, unique=True)
    content = models.CharField(max_length=10, null=False)
    
    class Meta:
        db_table = "textbox"