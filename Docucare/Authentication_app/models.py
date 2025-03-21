from django.db import models
from django.utils import timezone
import uuid


class Patient_Info(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, blank=False)
    phone = models.TextField(null=False,blank=False,unique=True)
    gender = models.TextField(null=False,blank=False)
    age = models.IntegerField(null=False,blank=False)
    place = models.TextField(null=False,blank=False)
    date_created = models.DateTimeField(default=timezone.now)
    

    def __str__(self):
        return self.username