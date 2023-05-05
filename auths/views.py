from lib2to3.pgen2 import token
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from accounts.models import User
import datetime

from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied

class CustomTokenRefreshView(TokenRefreshView):
    def check_token_blacklist(self, token):
        try:
            super().check_token_blacklist(token)
        except AuthenticationFailed as e:
            if 'Token is blacklisted' in str(e):
                # 토큰 만료 시 403 Forbidden 반환
                raise PermissionDenied('Token is expired', code='token_expired')
            else:
                raise


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh':str(refresh),
        'access':str(refresh.access_token),
    }

def get_user_from_access_token(access_token):
    try:
        access_token_obj = AccessToken(access_token)
        access_token_obj.check_exp()
    except(TokenError, InvalidToken):
        # response_data = {'error':'Token is expired or invalid.'}
        return None
    
    user_id=access_token_obj['user_id']
    
    try:
        user=User.objects.get(id=user_id)
        return user
    except:
        return None
    

def get_generation():
    today = datetime.today()
    year = today.year
    generation = year - 2012
    
    return generation
        
    
    

    