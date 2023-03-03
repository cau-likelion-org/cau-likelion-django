from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

urlpatterns = [
    # path('', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', TokenRefreshView.as_view(), name='token_refresh'),
]
