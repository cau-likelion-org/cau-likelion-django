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

# 0 : default, 1 : 출석 , 2 : 지각, 3 : 무단 결석
# 지각: tardiness, 결석: absence, 무단결석: truancy

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
            
            

class AttendanceView(APIView):
    # 개별 출석 처리 + 지각 처리
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        today = datetime.now().date()
        now = datetime.now()

        attendance = Attendance.objects.get(date=today)
        
        # 비밀번호가 틀린 경우
        if attendance.password != request.data['password']:
            return JsonResponse('비밀번호가 틀렸습니다.', status=400)

        
        user = User.objects.get(access_token=token)
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
        date = request.get('date')
        
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
            

class AttendanceModifyView(APIView):
    permission_classes = [IsManagementTeam]

    # 인정 결석 -> 운영진이 수정
    # input : user id (pk), 출석부 날짜, 출석부 key value
    def post(self, request):
        user_id = request.get('user_id')
        date = request.get('date')
        attendance_result = request.get('attendance_result')
        
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
        

        
                
                
        