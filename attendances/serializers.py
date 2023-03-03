from dataclasses import field
from rest_framework.serializers import ModelSerializer

from accounts.models import User
from .models import Attendance, UserAttendance

class AttendanceSerializer(ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

class UserAttendanceSerializer(ModelSerializer):
    class Meta:
        model = UserAttendance
        fields = [
            'time',
            'attendance_result'
        ]