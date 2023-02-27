from os import access
from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.models import User
import jwt
from django.conf import settings
from auths.views import *

class IsManagementTeam(BasePermission):

    def has_permission(self, request, view):
        token = request.META.get('HTTP_AUTHORIZATION')
        user = get_user_from_access_token(token)
        # user = User.objects.get(access_token = token)
        # payload = jwt.decode(token, settings.WEF_KEY, algorithms='HS256')
        # user = User.objects.get(id=payload.get('id'))
        if user.is_admin != True:
            return False
        return True
        