from django.http import JsonResponse
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from config.permissions import IsManagementTeam
from .serializers import AttendanceSerializer, UserAttendanceSerializer
from accounts.models import User
from .models import *
from datetime import datetime
from auths.views import *

# 0 : default, 1 : 출석 , 2 : 지각, 3 : 무단 결석
# 지각: tardiness, 결석: absence, 무단결석: truancy

# 운영진 only - get, post
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
        
        return Response(data={
            "message" : "success",
            "data" : attendance.data
        }, status=status.HTTP_200_OK)
    
    # 전체 출석부 조회 - 날짜별로 나눠서 return
    def get(self, request):
        attendances = Attendance.objects.all()
        
        attendances_list = []
        
        # 날짜 별 출석 현황 전체 반환 
        for attendance in attendances:
            user_attendances = UserAttendance.objects.filter(attendance=attendance)
            
            user_attendances_list = []
            
            for user_attendance in user_attendances:
                user_attendance_json = {
                    "name" : user_attendance.user.name,
                    "track" : user_attendance.user.track,
                    "attendance_result" : user_attendance.attendance_result
                }
                user_attendances_list.append(user_attendance_json)
            
            attendance_json = {
                "date" : attendance.date,
                "data" : user_attendances_list
            }
            
            attendances_list.append(attendance_json)
        
        return Response(data={
            "message" : "success",
            "data" : attendances_list
        }, status=status.HTTP_200_OK)
            
            
# get, post
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
        
        time = now - datetime.strptime(now.strftime("%Y%m%d"), "%Y%m%d")
        
        if time.seconds < 68700:
            user_attendance.time = time
            user_attendance.attendance_result = 1
            user_attendance.save()
        else:
            user_attendance.time = time
            user_attendance.attendance_result = 2
            user_attendance.save()
        
        return Response(data={
            'message' : 'success',
            'data': {
                'name':user.name,
                'track':user.track,
                'attendance_result':user_attendance.attendance_result
            }
        }, status=status.HTTP_200_OK)
    
    # 오늘의 출석부
    # input : date
    # output : name, attendance_result
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
                
                user_attendance_json = {
                        "name" : user_attendance.user.name,
                        "attendance_result" : user_attendance.attendance_result
                }
                
                # 기획
                if user_attendance.user.track == 0:
                    PM.append(user_attendance_json)
                
                # 디자인
                if user_attendance.user.track == 1:
                    DGN.append(user_attendance_json)
                
                # 프론트
                if user_attendance.user.track == 2:
                    FE.append(user_attendance_json)
                    
                # 백엔드
                if user_attendance.user.track == 3:
                    BE.append(user_attendance_json)
        
        return Response(data={
            "message" : "success",
            "data" : {
                "0" : PM,
                "1" : DGN,
                "2" : FE,
                "3" : BE
            }
        }, status=status.HTTP_200_OK)
            
# post
# 인정 결석 -> 운영진이 수정
class AttendanceModifyView(APIView):
    permission_classes = [IsManagementTeam]

    # input : user id (pk), 출석부 날짜, 출석부 key value
    def post(self, request):
        user_id = request.data['user_id']
        date = request.data['date']
        attendance_result = request.data['attendance_result']
        
        user = User.objects.get(pk=user_id)
        attendance = Attendance.objects.get(date=date)
        
        user_attendance = UserAttendance.objects.get(user=user, attendance=attendance)
        
        user_attendance.attendance_result = attendance_result
        user_attendance.save()
        
        updated_attendance_json = {
            "name" : user_attendance.user.name,
            "date" : user_attendance.attendance.date,
            "attendance_result" : attendance_result
        }
        
        return Response(data={
            'message' : 'success',
            'data' : updated_attendance_json
        }, status=status.HTTP_200_OK)
  
# get      
# 누적 출석 현황
class MypageView(APIView):
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        user = get_user_from_access_token(token)
        
        # 운영진 -> 아기사자 전체 누적 출석
        if user.is_admin == True:
            members = User.objects.filter(generation=11, is_admin=False)
        
            total_attendances = []
            
            for member in members:
                user_attendances = UserAttendance.objects.filter(user=member)
                
                attendance = 0 # 출석
                tardiness = 0 # 지각
                absence = 0 # 결석
                truancy = 0 # 무단결석
                
                for user_attendance in user_attendances:
                    if user_attendance.attendance_result == 0:
                        absence += 1
                    if user_attendance.attendance_result == 1:
                        attendance += 1
                    if user_attendance.attendance_result == 2:
                        tardiness += 1
                    if user_attendance.attendance_result == 3:
                        truancy += 1
                
                attendance_json = {
                    "name" : user_attendance.user.name,
                    "track" : user_attendance.user.track,
                    "attendnace" : attendance,
                    "tardiness" : tardiness,
                    "absence" : absence,
                    "truancy" : truancy
                }
                
                total_attendances.append(attendance_json)
            
            return Response(data={
                'message' : 'success',
                'data' : total_attendances
            }, status=status.HTTP_200_OK)
        
        # 아기사자 -> 본인 누적 출석 현황 조회
        else:
            user_attendances = UserAttendance.objects.filter(user=user)
            
            attendance = 0 # 출석
            tardiness = 0 # 지각
            absence = 0 # 결석
            truancy = 0 # 무단결석
            
            for user_attendance in user_attendances:
                if user_attendance.attendance_result == 0:
                    attendance += 1
                if user_attendance.attendance_result == 1:
                    tardiness += 1
                if user_attendance.attendance_result == 2:
                    absence += 1
                if user_attendance.attendance_result == 3:
                    truancy += 1
            
            user_attendance_json = {
                "name" : user.name,
                "attendance" : attendance,
                "tardiness" : tardiness,
                "absence" : absence,
                "truancy" : truancy
            }
                    
            return Response(data={
                'message' : 'success',
                'data' : user_attendance_json
            }, status=status.HTTP_200_OK)
        
        
        
        
        
        
                        
            

        

        
                
                
        