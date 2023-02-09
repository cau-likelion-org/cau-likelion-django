from dataclasses import field
from rest_framework.serializers import ModelSerializer
from .models import Attendance, UserAttendance

class AttendanceSerializer(ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'