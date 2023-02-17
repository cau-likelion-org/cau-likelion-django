from os import access
from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.models import User

class IsManagementTeam(BasePermission):

    def has_permission(self, request, view):
        token = request.META.get('HTTP_AUTHORIZATION')
        user = User.objects.get(access_token = token)
        if user.is_admin != True:
            return False
        return True
        