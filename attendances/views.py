from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from datetime import datetime

from config.permissions import IsManagementTeam
from .serializers import *
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
        
        date = request.data['date']
        password = request.data['password']
        
        attendances = Attendance.objects.all()
        for attendance in attendances:
            if str(attendance.date) == date:
                return Response(data={
                    "message" : "오늘의 출석부가 이미 생성되었습니다."
                }, status=status.HTTP_400_BAD_REQUEST)
        
        new_attendance = Attendance.objects.create(
            date = date,
            password = password
        )
        new_attendance.save()
        
        attendance_json = {
            "date" : new_attendance.date,
            "password" : new_attendance.password
        }
       
        # user별 출석부 create
        users = User.objects.filter(generation=11, is_admin=False)
        
        for user in users:
            new_user_attendance = UserAttendance.objects.create(
                user = user,
                attendance = new_attendance
            )
            new_user_attendance.save()
            
            user_cumulative_attendance = CumulativeAttendance.objects.get(user=user)
            user_cumulative_attendance.absence += 1 # 처음 출석부 생성되면 default 결석
            user_cumulative_attendance.save()
            
        
        return Response(data={
            "message" : "success",
            "data" : attendance_json
        }, status=status.HTTP_200_OK)
    

# '' : 개인 출석 체크, 개인 출석
class AttendanceView(APIView):
    # 출석 여부 체크
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        user = get_user_from_access_token(token)
        date = request.GET['date']
        
        date_result = datetime.strptime(date, "%Y-%m-%d")
        
        try:
            attendance = Attendance.objects.get(date=date_result)
            
            if user.is_admin == True:
                return Response(data={
                    "message" : "운영진 입니다."
                }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            else:
                if user.generation == 11:
                    user_attendance = UserAttendance.objects.get(user=user, attendance=attendance)
                    user_attendance_json = {
                        "name" : user.name,
                        "track" : user.track,
                        "date" : date,
                        "attendance_result" : user_attendance.attendance_result
                    }
                    
                    return Response(data={
                        "message" : "success",
                        "data" : user_attendance_json
                    }, status=status.HTTP_200_OK)
                else:
                    return Response(data={
                        "message" : "현재 활동중인 멤버가 아닙니다."
                    }, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(data={
                "message" : "출석부가 생성되지 않았습니다." # 세션 날 아닌 경우
            }, status=status.HTTP_400_BAD_REQUEST)
    
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
        user_cumulative_attendance = CumulativeAttendance.objects.get(user=user)
        
        time = now - datetime.strptime(now.strftime("%Y%m%d"), "%Y%m%d")
        
        
        # 6분부터 지각
        if time.seconds < 68760:
            user_attendance.attendance_result = 1
            user_attendance.save()
            
            user_cumulative_attendance.absence -= 1
            user_cumulative_attendance.save()
        else:
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
    
        
# /list : get - 오늘의 출석부
class AttendanceListView(APIView):
    
    # 오늘의 출석부
    def get(self, request):
        date = request.GET['date']
        
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
                "pm" : PM,
                "design" : DGN,
                "frontend" : FE,
                "backend" : BE
            }
        }, status=status.HTTP_200_OK)
            

        
        
        
        
        
        
                        
            

        

        
                
                
        