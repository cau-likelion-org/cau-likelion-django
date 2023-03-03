from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from datetime import datetime

from config.permissions import IsManagementTeam
from .serializers import AttendanceSerializer
from accounts.models import User
from .models import *
from mypages.models import *
from auths.views import *


# 0 : default, 1 : 출석 , 2 : 지각, 3 : 무단 결석
# 지각: tardiness, 결석: absence, 무단결석: truancy


# /secret : 오늘의 출석부 생성
class AttendanceAdminView(APIView):
    permission_classes = [IsManagementTeam]
    
    # 오늘의 패스워드 생성 + 오늘의 출석부 생성 (전체, 개인별)
    # password input
    def post(self, request):
        attendance = AttendanceSerializer(data=request.data)
        
        # 출석부 create
        if attendance.is_valid():
            attendance.save()
            
        
        # user별 출석부 create
        users = User.objects.filter(generation=11, is_admin=False)
        
        for user in users:
            new_user_attendance = UserAttendance.objects.create(
                user = user,
                attendance = attendance
            )
            new_user_attendance.save()
            
            user_cumulative_attendance = user.cumulativeattendance
            user_cumulative_attendance.absence += 1
            user_cumulative_attendance.save()
            
        
        return Response(data={
            "message" : "success",
            "data" : attendance.data
        }, status=status.HTTP_200_OK)
    
            

# / : post - 개인별 출석, get - 오늘의 출석부
class AttendanceView(APIView):
    # 개별 출석 처리 + 지각 처리
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        user = get_user_from_access_token(token)
        
        today = datetime.now().date()
        now = datetime.now()

        attendance = Attendance.objects.get(date=today)
        
        # 비밀번호가 틀린 경우
        if attendance.password != request.data['password']:
            return JsonResponse('비밀번호가 틀렸습니다.', status=400)

        user_attendance = UserAttendance.objects.get(attendance=attendance, user=user)
        user_cumulative_attendance = user.cumulativeattendance
        
        time = now - datetime.strptime(now.strftime("%Y%m%d"), "%Y%m%d")
        
        if time.seconds < 68700:
            user_attendance.time = time
            user_attendance.attendance_result = 1
            user_attendance.save()
            
            user_cumulative_attendance.absence -= 1
            user_cumulative_attendance.attendance += 1
            user_cumulative_attendance.save()
        else:
            user_attendance.time = time
            user_attendance.attendance_result = 2
            user_attendance.save()
            
            user_cumulative_attendance.absence -= 1
            user_cumulative_attendance.tardiness += 1
            user_cumulative_attendance.save()
        
        return Response(data={
            'message' : 'success',
            'data': {
                'name':user.name,
                'track':user.track,
                'attendance_result':user_attendance.attendance_result
            }
        }, status=status.HTTP_200_OK)
    
    # 오늘의 출석부
    def get(self, request):
        date = request.data['date']
        
        attendance = Attendance.objects.get(date=date) # 오늘 출석부
        user_attendances = UserAttendance.objects.filter(attendance=attendance)
        
        PM = []
        DGN = []
        FE = []
        BE = []
        
        for user_attendance in user_attendances:
            # 출석 or 지각
            if user_attendance.attendance_result == 1 or user_attendance.attendance_result == 2:
                
                # 기획
                if user_attendance.user.track == 0:
                    PM.append(user_attendance.user.name)
                
                # 디자인
                if user_attendance.user.track == 1:
                    DGN.append(user_attendance.user.name)
                
                # 프론트
                if user_attendance.user.track == 2:
                    FE.append(user_attendance.user.name)
                    
                # 백엔드
                if user_attendance.user.track == 3:
                    BE.append(user_attendance.user.name)
        
        return Response(data={
            "message" : "success",
            "data" : {
                "0" : PM,
                "1" : DGN,
                "2" : FE,
                "3" : BE
            }
        }, status=status.HTTP_200_OK)
            

        
        
        
        
        
        
                        
            

        

        
                
                
        