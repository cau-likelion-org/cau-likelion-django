from django.db import models

from accounts.models import User

# Create your models here.

class CumulativeAttendance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    tardiness = models.IntegerField(default=0, null=True, blank=True)
    absence = models.IntegerField(default=0, null=True, blank=True)
    truancy = models.IntegerField(default=0, null=True, blank=True)
    
