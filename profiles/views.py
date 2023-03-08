from accounts.serializers import *
from accounts.models import *
from auths.views import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

# '' : get - 유저 정보 조회, put - 정보 수정
class ProfileView(APIView):
    # 정보 조회
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        user = get_user_from_access_token(token)
        
        if user is None:
            return Response(data={
                "message" : "access_token으로 user를 찾을 수 없습니다."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if user.is_active == False:
            return Response(data={
                "message" : 'user is not activated yet'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserSerializer(user)
        
        return Response(data={
                "message" : 'success',
                "data" : {
                    "user" : serializer.data
                }
            }, status=status.HTTP_200_OK)
    
    # 정보 수정
    def put(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        user = get_user_from_access_token(token)
        
        if user.is_active == True: 
            update_serial = UserSerializer(user, data=request.data)
            
            if update_serial.is_valid():
                update_serial.save()
                
                serializer = UserSerializer(user)
                
                return Response(data={
                    "message" : 'success',
                    "data" : {
                        "user" : serializer.data
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response(data={
                    "message" : 'update_serial is not valid'
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={
                "message" : "This person is not a member yet."
            }, status=status.HTTP_400_BAD_REQUEST)
