from django.urls import path
from .views import *

urlpatterns = [
    path('attendance/', MypageAttendanceView.as_view()),
]
