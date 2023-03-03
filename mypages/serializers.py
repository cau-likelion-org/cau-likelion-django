from rest_framework.serializers import ModelSerializer

from accounts.models import User
from .models import CumulativeAttendance

class CumulativeAttendanceSerializer(ModelSerializer):
    class Meta:
        model = CumulativeAttendance
        fields = '__all__'