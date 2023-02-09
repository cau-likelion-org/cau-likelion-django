from os import access
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from config.permissions import IsManagementTeam
from .serializers import AttendanceSerializer, UserAttendanceSerializer
from rest_framework.permissions import IsAdminUser
from accounts.models import User
from .models import *
from datetime import datetime

class AttendancveViewSet(ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsManagementTeam]

attendance_list = AttendancveViewSet.as_view({
    'post':'create',
})

class AttendanceView(APIView):
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        today = datetime.now().date()
        now = datetime.now()

        attendance = Attendance.objects.get(date=today)
        #비밀번호가 틀린 경우
        if attendance.password != request.data['password']:
            return JsonResponse('비밀번호가 틀렸습니다.')

        user = User.objects.get(access_token=token)
        time = now - datetime.strptime(now.strftime("%Y%m%d"), "%Y%m%d")
        if time.seconds < 68700:
            new_user_attendance = UserAttendance.objects.create(
                user = user,
                attendance = attendance,
                time = time,
                is_completed = 1
            )
        elif time.seconds > 68700:
            new_user_attendance = UserAttendance.objects.create(
                user = user,
                attendance = attendance,
                time = time,
                is_completed = 2
            )
        
        return JsonResponse({
            'status':200,
            'success':True,
            'data':{
                'name':user.name,
                'track':user.track,
                'is_completed':new_user_attendance.is_completed
            }
        })


        