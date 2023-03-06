from django.db import models

from accounts.models import User

# Create your models here.

class Attendance(models.Model):
    date = models.DateField(null=True, blank=True)
    password = models.CharField(max_length=10, blank=True, null=True)

class UserAttendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    attendance_result = models.IntegerField(default=0)