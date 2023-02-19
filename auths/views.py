from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from accounts.models import User

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh':str(refresh),
        'access':str(refresh.access_token),
    }

def get_user_from_access_token(access_token):
    access_token_obj = AccessToken(access_token)
    user_id=access_token_obj['user_id']
    user=User.objects.get(id=user_id)
    return user