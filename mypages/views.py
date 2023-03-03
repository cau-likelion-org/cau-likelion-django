from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from auths.views import *
from accounts.models import *
from attendances.models import *
from accounts.serializers import *
from attendances.serializers import AttendanceSerializer, UserAttendanceSerializer

# Create your views here.

# '/attendance' : get - 누적 출석 조회, post - 출석 수정
class MypageAttendanceView(APIView):
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        user = get_user_from_access_token(token)
        
        # 운영진 -> 아기사자 전체 누적 출석
        if user.is_admin == True:
            members = User.objects.filter(generation=11, is_admin=False)
        
            total_attendances = []
            
            for member in members:
                cumulative_attendance = member.cumulativeattendance
                
                cumulative_attendance_json = {
                    "name" : cumulative_attendance.user.name,
                    "track" : cumulative_attendance.user.track,
                    "attendnace" : cumulative_attendance.attendance,
                    "tardiness" : cumulative_attendance.tardiness,
                    "absence" : cumulative_attendance.absence,
                    "truancy" : cumulative_attendance.truancy
                }
                
                total_attendances.append(cumulative_attendance_json)
            
            return Response(data={
                'message' : 'success',
                'data' : total_attendances
            }, status=status.HTTP_200_OK)
        
        # 아기사자 -> 본인 누적 출석 현황 조회
        else:
            user_cumulative_attendance = user.cumulativeattendance
            user_cumulative_attendance_json = {
                "name" : user.name,
                "attendance" : user_cumulative_attendance.attendance,
                "tardiness" : user_cumulative_attendance.tardiness,
                "absence" : user_cumulative_attendance.absence,
                "truancy" : user_cumulative_attendance.truancy
            }
                    
            return Response(data={
                'message' : 'success',
                'data' : user_cumulative_attendance_json
            }, status=status.HTTP_200_OK)
    
    # 누적 출석 수정 - input : user pk
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        user = get_user_from_access_token(token)
        
        member_id = request.data['user_id']
        attendance = request.data['attendance']
        tardiness = request.data['tardiness']
        absence = request.data['absence']
        truancy = request.data['truancy']
        
        member = User.objects.get(pk=member_id)
        
        if user.is_admin == True:
            cumulative_attendance = member.cumulativeattendance
            cumulative_attendance.attendance = attendance
            cumulative_attendance.tardiness = tardiness
            cumulative_attendance.absence = absence
            cumulative_attendance.truancy = truancy
            cumulative_attendance.save()
            
            cumulative_attendance_json = {
                "user_id" : cumulative_attendance.user.pk,
                "attendance" : cumulative_attendance.attendance,
                "tardiness" : cumulative_attendance.tardiness,
                "absence" : cumulative_attendance.absence,
                "truancy" : cumulative_attendance.truancy
            }
            
            return Response(data={
                "message" : "success",
                "data" : cumulative_attendance_json
            }, status=status.HTTP_200_OK)
        else:
            return Response(data={
                "message" : "You don't have permission."
            }, status=status.HTTP_400_BAD_REQUEST)
            
        
            
            
        

    
        
        
        
        
        
