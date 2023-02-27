from django.shortcuts import render, redirect
from accounts.serializers import UserSerializer
from auths.views import *

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.google import views as google_view
from rest_framework_simplejwt.serializers import RefreshToken
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from json import JSONDecodeError
from django.http import HttpResponse, JsonResponse

import requests
from datetime import datetime
from rest_framework import status

from .models import *
from .serializers import *

from allauth.socialaccount.models import SocialAccount


from rest_framework.views import APIView
from rest_framework.response import Response

import uuid
import jwt
import json

BASE_URL = 'https://api.cau-likelion.org/'
GOOGLE_CALLBACK_URI = BASE_URL + 'api/accounts/google/callback/'

# request -> code, access token

# access 있을때 -> 소셜로그인 O, 회원가입 X / 로그인
# access 없을 때 -> 진짜 처음 소셜로그인 ('')

# access token & 이메일 인증 요청 -> 회원가입 / 로그인 + jwt 토큰 발급
def google_callback(request):
    client_id = '312850794943-rogubu1don9b5fgn7tjf4jrf4ri98vcs.apps.googleusercontent.com'
    client_secret = settings.CLIENT_SECRET
    body = json.loads(request.body.decode('utf-8'))
    code = body['code']
    state = 'state_parameter_passthrough_value'
    
    # 1. 받은 코드로 구글에 access token 요청
    token_req = requests.post(f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri=http://localhost:3000/google&state={state}")
    
    ### 1-1. json으로 변환 & 에러 부분 파싱
    token_req_json = token_req.json()
    error = token_req_json.get("error")

    ### 1-2. 에러 발생 시 종료
    if error is not None:
        raise JSONDecodeError(error)

    ### 1-3. 성공 시 access_token 가져오기
    access_token = token_req_json.get('access_token')
    #################################################################
    
    # 가져온 access_token으로 이메일값을 구글에 요청
    response = requests.get(f"https://oauth2.googleapis.com/tokeninfo?access_token={access_token}")
    status = response.status_code

    ### 2-1. 에러 발생 시 400 에러 반환
    if status != 200:
        return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)
    
    ### 2-2. 성공 시 이메일/소셜ID 가져오기
    user = response.json()
    email = user.get('email')
    sub = user.get('sub')

    
    # 전달 받은 social_id로 user가 있는지 확인
    if User.objects.filter(social_id=sub).exists():
        user_info = User.objects.get(social_id=sub)

        # 소셜 로그인만 하고 회원가입은 안한 사람은 False로, 회원가입까지 한 사람은 True로 return
        if user_info.is_active == False:
            token = get_tokens_for_user(user_info)
            return JsonResponse({
                'token':token,
                'is_active':user_info.is_active
            }, status=200)
        else:
            token = get_tokens_for_user(user_info)
            return JsonResponse({
                'token':token,
                'is_active':user_info.is_active
            })
    # 아예 회원가입 안한 사람
    else:
        # 이메일이 @likelion.org 아닌 경우 오류 처리
        if email.split('@')[1] != 'likelion.org':
            return JsonResponse({'err_msg' : 'no matching likelion'}, status=status.HTTP_400_BAD_REQUEST)
        
        new_user_info = User.objects.create(
            social_id = sub,
            email = email
        )
        new_user_info.save()
        token = get_tokens_for_user(new_user_info)
        return JsonResponse({
            'token':token,
            'is_active':new_user_info.is_active
        })

# 추가 정보 기입

@method_decorator(csrf_exempt, name="dispatch")
class ProfileView(APIView):
    serializer_class = UserSerializer
# 초기 사용자 -> 회원 정보 넘어온 데이터로 update
    def put(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        user = get_user_from_access_token(token)

        update_serial = UserSerializer(user, data=request.data)
    
        if update_serial.is_valid():
            update_serial.save()
            
            # 아이디 활성화
            user.is_active = True
            user.save()
            
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
            
# 기사용자 -> 회원 정보 return
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        user = get_user_from_access_token(token)
        
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
        


# 인증코드 uuid 생성 (uuid1 : HostID, 현재 시간)
def create_code():
    result = str(uuid.uuid1())
    return result

# 학교 메일 인증
def cau_authentication(email):
    global code
    code = create_code()
    html_content = render_to_string('accounts/mail_template.html', {
        "code":code
    })
    to_email = email
    subject = "[중앙대 멋사] 학교 계정 확인 메일 🦁"
    content = "내용"
    sender_email = settings.EMAIL_HOST_USER
    send_mail(subject, content, sender_email, [to_email], html_message=html_content)
    
    return code

@method_decorator(csrf_exempt, name="dispatch")
class CauMailView(APIView):
    def get(self, request):
        email = request.GET.get('email')
        code = cau_authentication(email)
        token = request.META.get('HTTP_AUTHORIZATION')
        user = get_user_from_access_token(token)
        user.code = code
        user.save()
        return JsonResponse({
            'code' : code,
        }, safe=False, status = 200)
    
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        user = get_user_from_access_token(token)
        code = user.code
        if request.data['code'] != code:
            return Response(False)
        return Response(True)
