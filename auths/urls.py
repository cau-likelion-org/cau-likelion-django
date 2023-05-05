from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

urlpatterns = [
    path('/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
