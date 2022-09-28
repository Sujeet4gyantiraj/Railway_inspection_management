from django.db import models
import datetime
from django.utils import timezone

# Create your models here.
class MessageInsp(models.Model):
    message_no=models.BigAutoField(primary_key=True)
    message_to=models.ForeignKey('myadmin.Level_Desig', on_delete=models.CASCADE, null=True)
    message_sent=models.CharField(max_length=500, blank=False, null=True)
    message_reply=models.CharField(max_length=500, blank=False, null=True)
    message_by=models.CharField(max_length=15, blank=False, null=True)
    message_on = models.DateTimeField(auto_now_add=True, null=True)
    delete = models.BooleanField(default=False) 
