from django.contrib import admin
from .models import CumulativeAttendance

# Register your models here.

@admin.register(CumulativeAttendance)
class CumulativeAttendanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'attendance', 'tardiness', 'absence', 'truancy']