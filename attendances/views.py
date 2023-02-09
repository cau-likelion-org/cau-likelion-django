from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .serializers import AttendanceSerializer
from accounts.models import User
from .models import *
import datetime

class AttendancveViewSet(ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

attendance_list = AttendancveViewSet.as_view({
    'post':'create',
})

class AttendanceView(APIView):
    def post(request):
        token = request.META.get('HTTP_AUTHORIZATION')
        today = datetime.datatime.now().date()
        now = datetime.datatime.now()
        attendance = Attendance.objects.get(date=today)

        #비밀번호가 틀린 경우
        if attendance.password != request.data['password']:
            return JsonResponse('비밀번호가 틀렸습니다.')

        user = User.objects.get(access_token=token)
        time = now - today

        new_user_attendance = UserAttendance.objects.create(
            user = user,
            attendance = attendance,
            time = time,
            is_completed = 1
        )
        
        return JsonResponse({
            'status':200,
            'success':True,
            'data':{
                'name':user.name,
                'track':user.track,
            }
        })


        