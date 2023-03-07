from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import *
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
        
        if user.generation == 11:
            # 운영진 -> 아기사자 전체 누적 출석
            if user.is_admin == True:
                members = User.objects.filter(generation=11, is_admin=False)
            # generation 현재 - 2012 
                total_attendances = []
                
                for member in members:
                    cumulative_attendance = CumulativeAttendance.objects.get(user=member)
                
                    cumulative_attendance_json = {
                        "user_id" : member.pk,
                        "name" : cumulative_attendance.user.name,
                        "track" : cumulative_attendance.user.track,
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
                user_cumulative_attendance = CumulativeAttendance.objects.get(user=user)
                user_cumulative_attendance_json = {
                    "user_id" : user.pk,
                    "name" : user.name,
                    "tardiness" : user_cumulative_attendance.tardiness,
                    "absence" : user_cumulative_attendance.absence,
                    "truancy" : user_cumulative_attendance.truancy
                }
                        
                return Response(data={
                    'message' : 'success',
                    'data' : user_cumulative_attendance_json
                }, status=status.HTTP_200_OK)
        else:
            return Response(data={
                "message" : "현재 활동중인 회원이 아닙니다."
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    # 누적 출석 수정 - input : user pk
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        user = get_user_from_access_token(token)
        
        member_id = request.data['user_id']
        tardiness = request.data['tardiness']
        absence = request.data['absence']
        truancy = request.data['truancy']
        
        try:
            member = User.objects.get(pk=member_id)
        except:
            return Response(data={
                "message" : "가입되지 않은 회원입니다."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        
        if user.is_admin == True:
            cumulative_attendance = CumulativeAttendance.objects.get(user=member)
            cumulative_attendance.tardiness = tardiness
            cumulative_attendance.absence = absence
            cumulative_attendance.truancy = truancy
            cumulative_attendance.save()
            
            cumulative_attendance_json = {
                "user_id" : cumulative_attendance.user.pk,
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
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        
            
            
        

    
        
        
        
        
        
