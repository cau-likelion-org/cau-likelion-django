from lib2to3.pgen2 import token
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from accounts.models import User
from .models import *
import datetime

def create_password(request):
    if request.method == "POST":
        token = request.META.get('HTTP_AUTHORIZATION')
        user = User.objects.get(access_token=token)
        
        if user.is_admin != True:
            return JsonResponse('운영진만 접근할 수 있습니다.')
        
        new_attendance = Attendance.objects.create(
            password = request.data['password'],
        )

        return JsonResponse({
            'status':200,
            'success':True,
            'message':'출석부 생성 성공'
        })

    return JsonResponse({
            'status':405,
            'success':False,
            'message':'출석부 생성 실패'
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


        