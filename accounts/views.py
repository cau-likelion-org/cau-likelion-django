import email
from email.mime.text import MIMEText
from http.client import OK
import os
import re
from django.shortcuts import render, redirect
from accounts.serializers import UserSerializer

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.google import views as google_view
from rest_framework_simplejwt.serializers import RefreshToken
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

from json import JSONDecodeError
from django.http import HttpResponse, JsonResponse
import requests
from rest_framework import status
from .models import *
from allauth.socialaccount.models import SocialAccount

from django.core.mail import EmailMessage

from rest_framework.views import APIView

import uuid

BASE_URL = 'http://localhost:8000/'
GOOGLE_CALLBACK_URI = BASE_URL + 'api/accounts/google/callback/'

# request -> code, access token

# access 있을때 -> 소셜로그인 O, 회원가입 X / 로그인
# access 없을 때 -> 진짜 처음 소셜로그인 ('')

# access token & 이메일 인증 요청 -> 회원가입 / 로그인 + jwt 토큰 발급
def google_callback(request):
    client_id = '312850794943-rogubu1don9b5fgn7tjf4jrf4ri98vcs.apps.googleusercontent.com'
    client_secret = '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'
    code = request.GET.get('code')
    state = 'state_parameter_passthrough_value'
    access_token = request.data['access_token']
    
    if access_token == None:
        # 아예 처음 소셜로그인 하는 사람 -> 구글에 요청 필요
        # 1. 받은 코드로 구글에 access token 요청
        token_req = requests.post(f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}")
        
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
    email_req = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
    email_req_status = email_req.status_code

    ### 2-1. 에러 발생 시 400 에러 반환
    if email_req_status != 200:
        return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)
    
    ### 2-2. 성공 시 이메일 가져오기
    email_req_json = email_req.json()
    email = email_req_json.get('email')

    # return JsonResponse({'access': access_token, 'email':email})

    #################################################################

    # 전달받은 이메일, access_token, code를 바탕으로 회원가입/로그인
    try:
        # 전달받은 이메일로 등록된 유저가 있는지 탐색
        user = User.objects.get(email=email)
        
        if user.is_active == False:
            # active 안된거면 -> 소셜로그인은 했는데, 회원 가입 안한 사람
            return JsonResponse({
                'is_active' : user.is_active
            })
        
        # 기 사용자 => 로그인 & 해당 유저의 jwt 발급
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(f"{BASE_URL}api/accounts/google/login/finish/", data=data)
        accept_status = accept.status_code

        # 뭔가 중간에 문제가 생기면 에러
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)

        accept_json = accept.json()
        accept_json.pop('user', None)
        
        return JsonResponse(accept_json)
    
    except User.DoesNotExist:
        # 전달받은 이메일로 기존에 가입된 유저가 아예 없으면 => 새로 회원가입 & 해당 유저의 jwt 발급
        # 이때 likelion & cau 메일 인증 필요
        
        # 이메일이 @likelion.org 아닌 경우 : status code, 에러로 처리
        if email.split('@')[1] != 'likelion.org':
            return JsonResponse({'err_msg' : 'no matching likelion'}, status=status.HTTP_400_BAD_REQUEST)
        
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(f"{BASE_URL}api/accounts/google/login/finish/", data=data)
        accept_status = accept.status_code

        # 뭔가 중간에 문제가 생기면 에러
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)

        accept_json = accept.json()
        accept_json.pop('user', None)

        save_token(email, accept_json)
        
        return JsonResponse({
            'data' : accept_json,
            'is_active' : user.is_active
        })

# 토큰 저장
def save_token(email, token):
    user = User.objects.get(email=email)
    user.access_token = token.get('access_token')
    user.refresh_token = token.get('refresh_token')
    user.save()

# 구글 소셜 로그인 뷰
class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client

# 인증코드 uuid 생성
def create_code():
    result = str(uuid.uuid1())
    return result

# 학교 메일 인증
def cau_authentication(request):
    text_title = '[중앙대 멋사] 학교 계정 확인 메일 🦁'
    global code
    code = create_code()
    html_content = render_to_string('accounts/mail_template.html', {
        "code":code
    })
    to_email = request.data['email']
    subject = "제목"
    content = "내용"
    sender_email = settings.EMAIL_HOST_USER
    send_mail(subject, content, sender_email, [to_email], html_message=html_content)
    return code


# 초기 사용자 (is_active = False) 회원 정보 입력 (patch)
# 기사용자 (is_active = True) 회원 정보 return


# 추가 정보 기입
class UserView(APIView):

# 초기 사용자 -> 회원 정보 넘어온 데이터로 update
    def patch(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        user = User.objects.get(access_token=token)
        
        if user.is_active == False:
            user.name = request.data['name']
            user.generation = request.data['generation']
            user.track = request.data['track']
            user.is_admin = request.data['is_admin']
            user.is_active = True
            user.save()
            
        return JsonResponse({
            'name':user.name,
            'generation':user.generation,
            'track':user.track,
            'is_admin':user.is_admin,
        })

# 기사용자 -> 회원 정보 return
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        user = User.objects.get(access_token=token)
        
        if user.is_active == True:
            return JsonResponse({
                'name' : user.name,
                'generation' : user.generation,
                'track' : user.track,
                'is_admin' : user.is_admin
            })

class CauMailView(APIView):
    
    def get(self, request):
        code = cau_authentication(request)
        token = request.META.get('HTTP_AUTHORIZATION')
        print(token)
        user = User.objects.get(access_token = token)
        user.code = code
        user.save()
        return JsonResponse({
            'code':code,
        }, safe=False)
    
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        code = User.objects.get(access_token = token).code
        if request.data['code'] != code:
            return JsonResponse('False', safe=False)
        return JsonResponse('True', safe=False)
