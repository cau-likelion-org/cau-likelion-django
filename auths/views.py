from lib2to3.pgen2 import token
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from accounts.models import User

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
        response_data = {'error':'Token is expired or invalid.'}
        return JsonResponse(response_data, status=401)
    user_id=access_token_obj['user_id']
    user=User.objects.get(id=user_id)
    return user

    