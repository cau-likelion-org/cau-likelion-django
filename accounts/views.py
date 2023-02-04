from http.client import OK
import os
from django.shortcuts import render, redirect
from accounts.serializers import UserSerializer
##
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.google import views as google_view

from json import JSONDecodeError
from django.http import HttpResponse, JsonResponse
import requests
from rest_framework import status
from .models import *
from allauth.socialaccount.models import SocialAccount

import random
import string

from django.core.mail import EmailMessage

from rest_framework.views import APIView

BASE_URL = 'http://localhost:8000/'
GOOGLE_CALLBACK_URI = BASE_URL + 'api/accounts/google/callback/'


# 구글 로그인
# 구글 로그인 창 나옴 & 로그인 후 callback url로 코드값 반환
def google_login(request):
    scope = "https://www.googleapis.com/auth/userinfo.email"
    client_id = '312850794943-rogubu1don9b5fgn7tjf4jrf4ri98vcs.apps.googleusercontent.com'
    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")



# access token & 이메일 인증 요청 -> 회원가입 / 로그인 + jwt 토큰 발급
def google_callback(request):
    client_id = '312850794943-rogubu1don9b5fgn7tjf4jrf4ri98vcs.apps.googleusercontent.com'
    client_secret = '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'
    code = request.GET.get('code')
    state = 'state_parameter_passthrough_value'
    
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

    # 2. 가져온 access_token으로 이메일값을 구글에 요청
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

    # 3. 전달받은 이메일, access_token, code를 바탕으로 회원가입/로그인
    try:
        # 전달받은 이메일로 등록된 유저가 있는지 탐색
        user = User.objects.get(email=email)
        
        # Google & likelion으로 가입된 유저 => 로그인 & 해당 유저의 jwt 발급
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
        
        # 이메일이 @likelion.org 아닌 경우 오류 처리
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
        
        return JsonResponse(accept_json)

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

# 난수 6자리 생성
def authentication_num():
    LENGTH = 6
    string_pool = string.digits
    result = ""
    for _ in range(LENGTH):
        result += random.choice(string_pool)
    return result

# 학교 메일 인증
def cau_authentication(request):
    text_title = '[중앙대 멋사] 학교 계정 확인 메일 🦁'
    global authentication_num
    authentication_num = authentication_num()
    text_content = '다음 인증 번호를 입력하여 회원 가입을 계속 진행해주세요\n' + authentication_num
    email = EmailMessage(text_title, text_content, to=[request.data['email']])
    result = email.send()
    return authentication_num

# 회원가입 -> 인증번호 요청 버튼 누를 때
class UserView(APIView):
    def post(self, request):
        global authentication_num
        authentication_num  = cau_authentication(request)

        new_user = User.objects.create(
            name = request.data['name'],
            generation = request.data['generation'],
            email = request.data['email'],
            department = request.data['department'],
            access_token = request.headers.get('access-token'),
            refresh_token = request.headers.get('refresh-token'),
            authentication_number = authentication_num
        )
        # serializer = UserSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return JsonResponse('success', safe=False)
        return JsonResponse({
            'name':new_user.name
        })

        