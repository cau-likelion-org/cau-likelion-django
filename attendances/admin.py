from django.contrib import admin
from .models import Attendance, UserAttendance
# Register your models here.

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'password']

class UserAttendance(admin.ModelAdmin):
    list_display = ['id', 'time', 'user', 'attedance','is_completed']